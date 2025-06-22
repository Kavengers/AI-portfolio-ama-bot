# app/api/v1/routes.py
from fastapi import APIRouter, HTTPException
from app.services.embedding import get_embedding
from app.core.vector_store import collection
from app.models.item import InputText

router = APIRouter()

@router.get("/ping")
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
        n_results=n_results,
        include=["distances", "metadatas"]
    )
    distances = results["distances"][0]
    best_distance = distances[0]
    # SIMILARITY_THRESHOLD = 0.3

    # if best_distance >= SIMILARITY_THRESHOLD:
    #     raise HTTPException(status_code=404, detail="Oops! I don't think i have answer to that right now. But you can download my resume to get any information you need about me.")

    return {
        "metadata": results["metadatas"][0][0],
        "score": 1 - best_distance  # optional: convert to similarity score
    }
