import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from config import (
    EMBEDDING_MODEL, PINECONE_API_KEY,
    PINECONE_INDEX_NAME, TOP_K, EMBEDDING_DIMENSION
)

_embeddings = None
_vectorstore = None


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        print("Loading embedding model...")
        _embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return _embeddings


def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        from pinecone import Pinecone
        from langchain_community.vectorstores import Pinecone as LangchainPinecone

        print("Connecting to Pinecone...")
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(PINECONE_INDEX_NAME)
        embeddings = get_embeddings()

        _vectorstore = LangchainPinecone(
            index=index,
            embedding=embeddings,
            text_key="text"
        )
        print("Pinecone vectorstore ready.")
    return _vectorstore


def get_retriever():
    vs = get_vectorstore()
    if vs is None:
        return None
    return vs.as_retriever(search_kwargs={"k": TOP_K})


def add_documents(chunks: list[Document]) -> int:
    global _vectorstore
    from pinecone import Pinecone
    from langchain_community.vectorstores import Pinecone as LangchainPinecone

    embeddings = get_embeddings()
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX_NAME)

    print(f"Adding {len(chunks)} chunks to Pinecone...")

    if _vectorstore is None:
        _vectorstore = LangchainPinecone(
            index=index,
            embedding=embeddings,
            text_key="text"
        )

    # Add documents directly through the index
    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    _vectorstore.add_texts(texts=texts, metadatas=metadatas)

    print(f"Successfully added {len(chunks)} chunks to Pinecone.")
    return len(chunks)


def reset_vectorstore():
    global _vectorstore
    from pinecone import Pinecone

    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX_NAME)
    index.delete(delete_all=True)
    _vectorstore = None
    print("Pinecone index cleared.")