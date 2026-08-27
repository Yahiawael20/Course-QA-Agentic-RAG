# 🎓 Course QA Agent - Agentic RAG

An Agentic Retrieval-Augmented Generation (RAG) system that answers questions about educational course materials using AI.

The system retrieves relevant information from course documents, plans how to answer the user's question, selects the appropriate tool, and generates an accurate response based only on the provided course materials.

---

## 🚀 Features

-  Retrieval-Augmented Generation (RAG)
-  AI Planner for tool selection
-  Semantic search using FAISS
-  Course summarization
-  Concept comparison
-  Quiz generation
-  Source citation with page numbers
-  Rejects questions outside the provided documents
-  Answers only from course materials

---

## 📂 Available Courses

- Python
- Artificial Intelligence
- Machine Learning
- Deep Learning

---

## 🛠️ Tech Stack

- Python
- LangChain
- FAISS
- HuggingFace Embeddings (BAAI/bge-base-en-v1.5)
- Groq LLM
- Streamlit

---

## 🧠 Agent Workflow

```text
User Question
      │
      ▼
Planner
      │
      ▼
Select Tool
      │
      ▼
Tool Execution
      │
      ▼
Retriever
      │
      ▼
FAISS Vector Store
      │
      ▼
Relevant Context
      │
      ▼
LLM
      │
      ▼
Final Answer
```

---

## 🔧 Supported Tools

### 🔎 Retrieval Tool

Answers factual questions using the course materials.

Example:

- What is Deep Learning?
- What is Gradient Descent?

---

### 📝 Summary Tool

Generates concise summaries.

Example:

- Summarize Gradient Descent
- Summarize Neural Networks

---

###  Compare Tool

Compares two concepts using information retrieved from the documents.

Example:

- Compare Machine Learning and Deep Learning
- Compare CNN and RNN

---

###  Quiz Tool

Generates multiple-choice questions from the course materials.

Example:

- Create a quiz about Machine Learning
- Test me on Python

---

## 📁 Project Structure

```text
Course_QA_Agent/
│
├── agent/
│   ├── agent.py
│   └── planner.py
│
├── data/
│
├── sources/
│   ├── embeddings.py
│   ├── llm.py
│   ├── loaders.py
│   ├── rag.py
│   ├── retriever.py
│   ├── splitter.py
│   └── vector_store.py
│
├── tools/
│   ├── retrieval_tool.py
│   ├── summary_tool.py
│   ├── compare_tool.py
│   └── quiz_tool.py
│
├── vector_store/
│
├── app.py
├── build_index.py
├── test_agent.py
└── requirements.txt
```

---

## ▶️ How It Works

1. Load course PDFs.
2. Split documents into chunks.
3. Generate embeddings.
4. Store embeddings in FAISS.
5. User asks a question.
6. The Planner selects the appropriate tool.
7. The selected tool retrieves relevant context.
8. The LLM generates the final answer.
9. Sources and page numbers are returned.

---

## 📸 Demo

The application allows users to:

- Ask questions
- Summarize topics
- Compare concepts
- Generate quizzes
- View document sources
- See the Agent workflow

---

## 🎯 Example Questions

- What is Deep Learning?
- Summarize Gradient Descent.
- Compare for loop and while loop.


---

## 📌 Notes

- The assistant answers **only** from the provided course materials.
- If the requested information is not available in the documents, the assistant responds that it cannot find the answer.
- Every response includes the relevant document sources and page numbers.

