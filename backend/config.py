import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "geoscience-rag"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.3-70b-versatile"
FAISS_INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "faiss_index")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw_docs")
TOP_K = 5
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50
EMBEDDING_DIMENSION = 384