# app/core/vector_store.py
import chromadb
from chromadb.config import Settings

chroma_client = chromadb.PersistentClient(path="./chroma-data")

collection = chroma_client.get_or_create_collection(name="question_answers")
