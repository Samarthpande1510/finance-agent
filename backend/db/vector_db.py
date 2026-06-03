from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
import pandas as pd

data = pd.read_csv("db/transactions.csv")

client = QdrantClient(host="localhost",port=6333)
VECTOR_SIZE = 768
COLLECTION_NAME = "transactions"
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

descriptions = data["description"].tolist()
embeddings = model.encode(descriptions)


def init_collection():
    existing = client.get_collections().collections
    names = [c.name for c in existing]
    if COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE,distance=Distance.COSINE)
        )

def get_embedding(text: str,is_query: bool = False):
    if is_query:
        text = f"Represent this sentence for searching relevant passages: {text}"
    return model.encode(text).tolist()
    

def store_embedding(transaction_id: int, user_id: int, text: str, vector: list[float]):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=transaction_id,
                vector=vector,
                payload={"user_id": user_id, "text": text} 
            )
        ]
    )


def search(user_id: int, query_vector: list[float], limit: int = 5) -> list[dict]:
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=Filter(
            must=[FieldCondition(key="user_id", match=MatchValue(value=user_id))]
        ),
        limit=limit
    )
    return [{"transaction_id": r.id, "score": r.score, "text": r.payload["text"]} for r in results.points]


if __name__ == "__main__":
    init_collection()
    print("Collection ready")
    


for i, row in data.iterrows():
    vec = get_embedding(row["description"])
    store_embedding(i + 2, 1, row["description"], vec)

print("Stored all transactions")


queries = [
    "food delivery",
    "luxury shopping",
    "cab ride",
    "electronics"
]
for q in queries:
    query_vec = get_embedding(q, is_query=True)
    results = search(1, query_vec, limit=3)
    print(f"\n'{q}' →")
    for r in results:
        print(f"  {r['text']} (score: {r['score']:.3f})")