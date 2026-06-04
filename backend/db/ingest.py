import pandas as pd
from db.database import SessionLocal
from db.model import Transaction
from db.vector_store import get_embedding, store_embedding, init_collection
from datetime import datetime

def ingest_csv(file_path: str,user_id: int) -> dict:
    db = SessionLocal()
    try:
        init_collection()
        data = pd.read_csv(file_path)
        count = 0

        for _,row in data.iterrows():
            transaction = Transaction(
                user_id=user_id,
                amount=row["amount"],
                raw_description=row["description"],
                date=row["date"],
                agent_category=None
            )
            db.add(transaction)
            db.flush()

            vector = get_embedding(row["description"])

            store_embedding(transaction.id,user_id,row["description"],vector)

            count +=1
        
        db.commit()
        return {"ingested": count, "user_id": user_id}
    
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    result = ingest_csv("db/transactions.csv", user_id=1)
    print(result)


