from db.model import Transaction
from datetime import date
from sqlalchemy.orm import Session
def get_transactions(db: Session,user_id: int, start_date: str, end_date: str) -> list[dict]:
    transaction  = db.query(Transaction).filter(Transaction.user_id == user_id,Transaction.date >= start_date
                                                ,Transaction.date <= end_date).all()
    if not transaction:
        return []
    return [
    {
        "id": t.id,
        "user_id": t.user_id,
        "amount": float(t.amount),
        "raw_description": t.raw_description,
        "agent_category": t.agent_category,
        "date": str(t.date),
        "created_at": str(t.created_at)
    }
    for t in transaction
]

def categorize_transaction(db: Session, user_id: int, description: str, amount: float, category: str) -> dict:
    transaction = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.raw_description == description,
        Transaction.amount == amount
    ).first()
    
    if not transaction:
        return {}
    
    transaction.agent_category = category
    db.commit()
    db.refresh(transaction)
    
    return {
        "id": transaction.id,
        "raw_description": transaction.raw_description,
        "agent_category": transaction.agent_category
    }

def get_spending_summary(db: Session, user_id: int, start_date: str, end_date: str) -> dict:
    transaction = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).all()
    
    if not transaction:
        return {}
    
    total = sum(float(t.amount) for t in transaction)
    
    by_category = {}
    for t in transaction:
        cat = t.agent_category or "uncategorized"
        by_category[cat] = by_category.get(cat, 0) + float(t.amount)
    
    return {
        "total": round(total, 2),
        "by_category": by_category,
        "transaction_count": len(transaction),
        "period": {"start": start_date, "end": end_date}
    }

def detect_anomalies(db: Session, user_id: int):
    transaction = db.query(Transaction).filter(
        Transaction.user_id == user_id).all()
    
    if not transaction:
        return []
    
    total = sum(float(t.amount) for t in transaction)
    avg = total/len(transaction)

    flagged =[]
    for t in transaction:
        if float(t.amount) > (2*avg):
            flagged.append({
            "id": t.id,
            "description": t.raw_description,
            "amount": float(t.amount),
            "date": str(t.date),
            "average": round(avg, 2),
            "reason": "Transaction is significantly above your average spend"
        })
    
    return flagged

def search_spending_history(db: Session, user_id: int, query: str):
    transaction = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).all()

    if not transaction:
        return []
    match =[]
    for t in transaction:
        if (query in (t.raw_description or "").lower() or 
            query in (t.agent_category or "").lower()):
            match.append({
                "id": t.id,
                "raw_description": t.raw_description,
                "agent_category": t.agent_category,
                "amount": float(t.amount),
                "date": str(t.date)
            })

    return match
