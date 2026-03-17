import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from rag_chain import query as rag_query, reset_chain
from retriever import add_documents
from file_processor import (
    validate_uploads,
    extract_text_from_file,
    chunk_documents,
    MAX_FILES,
    MAX_TOTAL_SIZE_MB
)

app = FastAPI(
    title="RAG Geoscience Assistant API",
    description="Retrieval-Augmented Generation for Geoscience queries",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list


class UploadResponse(BaseModel):
    message: str
    files_processed: int
    chunks_added: int
    errors: list


@app.get("/")
def root():
    return {"message": "RAG Geoscience Assistant API v2.0 is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload", response_model=UploadResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    is_valid, message = validate_uploads(files)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    files_processed = 0
    total_chunks = 0
    errors = []

    for file in files:
        try:
            file_bytes = await file.read()
            documents = extract_text_from_file(file_bytes, file.filename)

            if not documents:
                errors.append(f"{file.filename}: No text could be extracted.")
                continue

            chunks = chunk_documents(documents)
            chunks_added = add_documents(chunks)
            total_chunks += chunks_added
            files_processed += 1
            print(f"Processed {file.filename}: {chunks_added} chunks added.")

        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")

    reset_chain()

    return UploadResponse(
        message=f"Successfully processed {files_processed} file(s).",
        files_processed=files_processed,
        chunks_added=total_chunks,
        errors=errors
    )


@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        result = rag_query(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/reset")
def reset_index():
    import shutil
    from config import FAISS_INDEX_PATH
    if os.path.exists(FAISS_INDEX_PATH):
        shutil.rmtree(FAISS_INDEX_PATH)
        os.makedirs(FAISS_INDEX_PATH)
    reset_chain()
    from retriever import _vectorstore
    import retriever
    retriever._vectorstore = None
    return {"message": "Index cleared. Upload new documents to start fresh."}