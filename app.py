
import streamlit as st
import os
import time
import streamlit.components.v1 as components

from auth import signup, login
from rag import process_pdf, retrieve_context, extract_text
from solver import solve_question
from knowledge_graph import generate_graph_from_text


# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="Complete DSA Assistant",
    page_icon="🤖",
    layout="wide"
)

os.makedirs("data", exist_ok=True)
os.makedirs("graph", exist_ok=True)


# ---------------------------------
# SESSION STATE
# ---------------------------------

defaults = {
    "logged_in": False,
    "username": "",
    "processed": False,
    "pdf_name": "",
    "chunk_count": 0,
    "topic_count": 0,
    "chat_sessions": {"Chat 1": []},
    "current_chat": "Chat 1",
    "chat_count": 1,
    "graph_text": "",
    "graph_created": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------------------------
# LOGIN AND SIGN UP
# ---------------------------------

if not st.session_state.logged_in:

    st.title("🤖 Complete DSA Assistant")
    st.write("Sign in or create an account to continue.")

    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    with login_tab:

        st.subheader("Login")

        login_username = st.text_input(
            "Username",
            key="login_username"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login", use_container_width=True):

            if login(login_username, login_password):

                st.session_state.logged_in = True
                st.session_state.username = login_username

                st.success("Login successful!")
                st.rerun()

            else:
                st.error("Invalid username or password.")

    with signup_tab:

        st.subheader("Create Account")

        new_username = st.text_input(
            "Create Username",
            key="new_username"
        )

        new_password = st.text_input(
            "Create Password",
            type="password",
            key="new_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )

        if st.button("Sign Up", use_container_width=True):

            if not new_username or not new_password:
                st.warning("Please fill in all fields.")

            elif new_password != confirm_password:
                st.error("Passwords do not match.")

            elif signup(new_username, new_password):
                st.success("Account created! Please login.")

            else:
                st.error("Username already exists.")

    st.stop()


# ---------------------------------
# MAIN DASHBOARD
# ---------------------------------

st.title("🤖 The Complete DSA Assistant")
st.caption("AI-powered Data Structures and Algorithms Learning Platform")

st.sidebar.title("Dashboard")

st.sidebar.write(
    f"Welcome, **{st.session_state.username}**!"
)

if st.sidebar.button("Logout", use_container_width=True):

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.rerun()


# ---------------------------------
# PDF UPLOAD AND PROCESSING
# ---------------------------------

st.sidebar.divider()
st.sidebar.subheader("📄 Upload DSA PDF")

uploaded_file = st.sidebar.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if st.sidebar.button("Process PDF", use_container_width=True):

    if uploaded_file is None:

        st.sidebar.warning("Please upload a PDF first.")

    else:

        try:

            file_path = os.path.join(
                "data",
                uploaded_file.name
            )

            with open(file_path, "wb") as file:
                file.write(uploaded_file.getbuffer())

            with st.spinner("Processing PDF..."):

                pdf_text = extract_text(file_path)

                if not pdf_text.strip():
                    raise ValueError(
                        "No readable text found in this PDF."
                    )

                chunks = process_pdf(file_path)

                generate_graph_from_text(
                    pdf_text,
                    uploaded_file.name
                )

                st.session_state.processed = True
                st.session_state.pdf_name = uploaded_file.name
                st.session_state.chunk_count = chunks
                st.session_state.graph_text = pdf_text
                st.session_state.graph_created = True

            st.sidebar.success("PDF processed successfully!")

        except Exception as e:

            st.sidebar.error(f"PDF processing failed: {e}")


if st.session_state.processed:

    st.sidebar.success(
        f"Processed: {st.session_state.pdf_name}"
    )

    st.sidebar.caption(
        f"Text chunks: {st.session_state.chunk_count}"
    )


# ---------------------------------
# CHAT HISTORY
# ---------------------------------

st.sidebar.divider()
st.sidebar.subheader("💬 Chat History")

if st.sidebar.button("➕ New Chat", use_container_width=True):

    st.session_state.chat_count += 1

    new_chat = f"Chat {st.session_state.chat_count}"

    st.session_state.chat_sessions[new_chat] = []
    st.session_state.current_chat = new_chat

    st.rerun()


chat_names = list(st.session_state.chat_sessions.keys())

selected_chat = st.sidebar.selectbox(
    "Select Conversation",
    chat_names,
    index=chat_names.index(st.session_state.current_chat)
)

if selected_chat != st.session_state.current_chat:

    st.session_state.current_chat = selected_chat
    st.rerun()


# ---------------------------------
# MAIN TABS
# ---------------------------------

tab1, tab2, tab3 = st.tabs(
    ["💬 Chat Assistant", "🧠 Knowledge Graph", "ℹ️ About"]
)


# ---------------------------------
# CHAT ASSISTANT
# ---------------------------------

with tab1:

    st.subheader("Ask Your DSA Question")

    if st.session_state.processed:

        st.info(
            f"Using uploaded PDF: {st.session_state.pdf_name}"
        )

    else:

        st.info(
            "You can ask questions without uploading a PDF. "
            "AI will generate answers and Knowledge Graphs."
        )

    messages = st.session_state.chat_sessions[
        st.session_state.current_chat
    ]

    for message in messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message.get("time"):
                st.caption(
                    f"Response time: {message['time']:.2f} seconds"
                )

    question = st.chat_input(
        "Ask anything about Data Structures and Algorithms..."
    )

    if question:

        messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        context = ""
        sources = []

        if st.session_state.processed:

            try:
                context, sources = retrieve_context(question)

            except Exception as e:
                st.warning(f"PDF retrieval issue: {e}")

        with st.chat_message("assistant"):

            with st.spinner("Generating answer..."):

                start_time = time.time()

                answer = solve_question(
                    question,
                    context
                )

                response_time = time.time() - start_time

            st.markdown(answer)

            st.caption(
                f"Response time: {response_time:.2f} seconds"
            )

            if sources:
                st.caption(
                    "Sources: " + ", ".join(sources)
                )

        # ---------------------------------
        # GENERATE GRAPH FOR LATEST QUESTION
        # ---------------------------------

        try:

            graph_content = (
                "Question: " + question
                + "\n\nAnswer: " + answer
            )

            # Replace old graph content with latest question.
            st.session_state.graph_text = graph_content

            generate_graph_from_text(
                graph_content,
                "Latest DSA Question"
            )

            st.session_state.graph_created = True

        except Exception as e:

            st.warning(
                f"Knowledge Graph generation issue: {e}"
            )

        messages.append({
            "role": "assistant",
            "content": answer,
            "time": response_time
        })

        st.rerun()


# ---------------------------------
# KNOWLEDGE GRAPH
# ---------------------------------

with tab2:

    st.subheader("🧠 DSA Knowledge Graph")

    st.write(
        "This graph displays relationships between DSA concepts "
        "from the latest question or uploaded PDF."
    )

    graph_file = "graph/knowledge_graph.html"

    if (
        st.session_state.graph_created
        and os.path.exists(graph_file)
    ):

        with open(graph_file, "r", encoding="utf-8") as file:
            graph_html = file.read()

        components.html(
            graph_html,
            height=650,
            scrolling=True
        )

    else:

        st.info(
            "Ask a DSA question or upload a PDF to generate "
            "your Knowledge Graph."
        )


# ---------------------------------
# ABOUT
# ---------------------------------

with tab3:

    st.subheader("About This Project")

    st.write("""
    The Complete DSA Assistant and Problem Solver is an
    AI-powered learning platform designed to help students
    understand Data Structures and Algorithms.

    **Main Technologies:**

    - Python
    - Streamlit
    - Gemini API
    - Retrieval-Augmented Generation (RAG)
    - ChromaDB
    - Sentence Transformers
    - NetworkX
    - PyVis
    - SQLite

    **Main Features:**

    - User Login and Sign Up
    - PDF Upload and Processing
    - AI-based Question Answering
    - Code Generation and Explanation
    - Knowledge Graph Visualization
    - Chat History
    - Response Time Measurement
    """)
