# 🌍 RAG-Powered Geoscience Assistant

> An AI assistant that answers geoscience questions grounded in real research 
> documents — no hallucinations, every answer is evidence-linked with source citations.

---

## 🚀 Live Demo

*Coming soon — deploying to HuggingFace Spaces*

---

## 🧠 What It Does

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline for the geoscience domain.

Instead of relying on an LLM's memorized knowledge, it:
1. Accepts uploaded documents (PDF, DOCX, TXT, XLSX)
2. Splits them into chunks and converts to vectors
3. Searches the vector database for relevant context
4. Feeds retrieved context to an LLM to generate a grounded, cited response

---

## 🏗️ Architecture
```
User Query → Streamlit UI → FastAPI Backend
                                   ↓
                        FAISS Vector Search
                                   ↓
                        Top-5 Relevant Chunks
                                   ↓
                       Groq LLM (Llama 3.3 70B)
                                   ↓
                     Answer + Source Citations
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| LLM | Groq API (Llama 3.3 70B) | Fast free inference |
| Embeddings | all-MiniLM-L6-v2 | Local, no API needed |
| Vector DB | FAISS | Similarity search |
| RAG Framework | LangChain | Pipeline orchestration |
| Backend | FastAPI | REST API |
| Frontend | Streamlit | Chat interface |

---

## 📁 Project Structure
```
rag-geoscience-assistant/
├── backend/
│   ├── main.py            # FastAPI app + endpoints
│   ├── ingest.py          # Document ingestion pipeline
│   ├── rag_chain.py       # RAG pipeline + LLM
│   ├── retriever.py       # FAISS vector search
│   ├── file_processor.py  # Multi-format file handler
│   └── config.py          # Configuration
├── frontend/
│   ├── app.py             # Streamlit chat UI
│   └── components.py      # UI components
├── data/
│   └── raw_docs/          # Upload PDFs here
├── tests/                 # Pytest test suite
├── app.py                 # HuggingFace Spaces entry
├── requirements.txt
└── Dockerfile
```

---

## 🚀 Run Locally

### Prerequisites
- Python 3.11
- Groq API key — free at [console.groq.com](https://console.groq.com)

### Setup
```bash
# Clone the repo
git clone https://github.com/Paras8-3-4/rag-geoscience-assistant.git
cd rag-geoscience-assistant

# Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your API key
echo GROQ_API_KEY=your_key_here > .env
```

### Run
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
streamlit run app.py
```

Open `http://localhost:8501`

---

## 📄 Supported File Formats

| Format | Extension |
|--------|-----------|
| PDF | .pdf |
| Word Document | .docx |
| Plain Text | .txt |
| Excel Spreadsheet | .xlsx, .xls |

**Limits:** Max 10 files · Max 150MB total size

---

## 🔬 Based On

Inspired by the research paper:
*"RAG-Powered Geoscience Assistant"* — Ghodichor et al., IRJMETS, November 2025

---

## 👤 Author

**Paras Lad**  
[GitHub](https://github.com/Paras8-3-4)

---

## 📜 License

MIT License — free to use and modify