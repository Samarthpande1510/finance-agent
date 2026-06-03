from db.database import SessionLocal
from db.model import User, Transaction, Budget
from datetime import date

def seed():
    db = SessionLocal()
    try:
        user = User(id=1, name="Samarth", email="samarth@test.com", hashed_password="fake")
        db.add(user)
        db.commit()

        transactions = [
            Transaction(user_id=1, amount=50.00, raw_description="Uber", agent_category="transport", date=date(2024, 3, 1)),
            Transaction(user_id=1, amount=120.00, raw_description="Zomato", agent_category="food", date=date(2024, 3, 5)),
            Transaction(user_id=1, amount=240.00, raw_description="Swiggy", agent_category="food", date=date(2024, 3, 6)),
            Transaction(user_id=1, amount=3400.00, raw_description="Gucci", agent_category="shopping", date=date(2024, 3, 7)),
            Transaction(user_id=1, amount=450.00, raw_description="Perfume", agent_category=None, date=date(2024, 4, 5)),
            Transaction(user_id=1, amount=560.00, raw_description="Whisky", agent_category=None, date=date(2024, 4, 6)),
            Transaction(user_id=1, amount=760.00, raw_description="Zomato", agent_category="food", date=date(2024, 4, 5)),
            Transaction(user_id=1, amount=80.00, raw_description="Ola", agent_category="transport", date=date(2024, 5, 1)),
            Transaction(user_id=1, amount=200.00, raw_description="Amazon", agent_category="shopping", date=date(2024, 5, 10)),
            Transaction(user_id=1, amount=5000.00, raw_description="Macbook repair", agent_category=None, date=date(2024, 5, 15)),
        ]

        db.add_all(transactions)
        db.add(Budget(user_id=1, category="food", amount=500.00))
        db.commit()
        print("seeded")
    finally:
        db.close()

if __name__ == "__main__":
    seed()