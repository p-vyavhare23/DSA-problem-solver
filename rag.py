
import os
import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

DATA_DIR = "data"
DB_DIR = "chroma_db"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection(name="dsa_documents")


def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    return "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    )


def split_text(text, chunk_size=700, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        chunk = text[start:start + chunk_size].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def process_pdf(pdf_file):

    # Get the PDF filename safely
    if hasattr(pdf_file, "name"):
        file_name = os.path.basename(pdf_file.name)
    else:
        file_name = os.path.basename(os.fspath(pdf_file))

    # Extract PDF text
    text = extract_text(pdf_file)

    if not text.strip():
        raise ValueError("No readable text found in PDF.")

    # Split text into chunks
    chunks = split_text(text)

    # Generate embeddings
    embeddings = model.encode(chunks).tolist()

    # Store chunks in ChromaDB
    collection.upsert(
        ids=[
            f"{file_name}_{i}"
            for i in range(len(chunks))
        ],
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {"source": file_name}
            for _ in chunks
        ]
    )

    return len(chunks)


def retrieve_context(question, k=4):

    query_embedding = model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    sources = list(dict.fromkeys(
        item.get("source", "Unknown")
        for item in metadatas
    ))

    return "\n\n".join(documents), sources
