# 💻 Complete DSA Assistant and Problem Solver

## 📌 About the Project

**Complete DSA Assistant and Problem Solver** is an AI-powered educational application designed to help students learn Data Structures and Algorithms (DSA), understand programming concepts, and solve coding problems efficiently.

It provides an intelligent assistant that helps users explore DSA topics, understand algorithms, and get solutions to programming problems using Google's Gemini AI.

## 🚀 Key Features

- **AI-Powered DSA Assistant:** Get answers to DSA-related questions.
- **DSA Concept Explanation:** Understand data structures and algorithms in an easy way.
- **Problem Solver:** Get assistance with solving programming problems.
- **Step-by-Step Solutions:** Understand the logic and approach behind solutions.
- **Knowledge Graph:** Explore relationships between DSA concepts.
- **PDF-Based Learning:** Uses DSA educational materials as a knowledge source.
- **RAG Integration:** Retrieves relevant information to provide context-aware answers.
- **User Authentication:** Login and registration functionality.

## 🛠️ Technologies Used

- Python
- Google Gemini API
- Retrieval-Augmented Generation (RAG)
- Knowledge Graph
- ChromaDB
- SQLite
- HTML
- CSS
- JavaScript

## 📂 Project Structure

```text
Complete-DSA-Assistant/
│
├── Data/
│   ├── DSA.pdf
│   └── DSA_Basics_for_Chatbot.pdf
│
├── graph/
│   └── knowledge_graph.html
│
├── lib/
│   ├── bindings/
│   ├── tom-select/
│   └── vis-9.1.2/
│
├── app.py
├── auth.py
├── knowledge_graph.py
├── rag.py
├── solver.py
├── test_gemini.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the Project Folder

```bash
cd Complete-DSA-Assistant
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Environment (Windows)

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Gemini API Key

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_api_key_here
```

Never upload your `.env` file or share your API key publicly.

### 7. Run the Application

```bash
python app.py
```

Open the local URL displayed in the terminal.

## 🎯 Project Objective

The objective of this project is to provide students with a complete AI-powered platform for learning Data Structures and Algorithms, understanding complex concepts, and solving programming problems with intelligent guidance.

## 👩‍💻 Project Category

Artificial Intelligence | Python | Data Structures and Algorithms | Problem Solving

---

**Complete DSA Assistant and Problem Solver**  
*Learn DSA. Understand Logic. Solve Problems Smarter.*
