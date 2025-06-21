# app/api/v1/routes.py
from fastapi import APIRouter
from app.services.embedding import get_embedding
from app.core.vector_store import collection
from app.models.item import InputText

router = APIRouter()

@router.get("/show")
def get_data():
    return {"status":"success"}

@router.post("/add")
def add_text(payload: InputText):
    embedding = get_embedding(payload.text)
    collection.add(
        documents=[payload.text],
        embeddings=[embedding],
        ids=[payload.text[:20]],  # naive ID
        metadatas=[payload.metadata]
    )
    return {"message": "Data added!"}

@router.get("/search")
def search_text(query: str, n_results: int = 3):
    embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )
    return {"results": results['metadatas'][0]}
