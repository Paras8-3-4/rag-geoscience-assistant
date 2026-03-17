import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import EMBEDDING_MODEL, FAISS_INDEX_PATH, DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP

def ingest_documents():
    print(f"Looking for PDFs in: {DATA_DIR}")

    if not os.listdir(DATA_DIR):
        print("ERROR: No PDF files found in data/raw_docs/")
        print("Please add at least one PDF file and run again.")
        return

    print("Loading PDFs...")
    loader = PyPDFDirectoryLoader(DATA_DIR)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from PDFs.")

    print("Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    print("Loading embedding model (first time may take a few minutes)...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    print("Building FAISS index...")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    print(f"Saving index to {FAISS_INDEX_PATH}...")
    vectorstore.save_local(FAISS_INDEX_PATH)
    print("Done! FAISS index saved successfully.")

if __name__ == "__main__":
    ingest_documents()