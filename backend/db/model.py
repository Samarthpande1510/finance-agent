from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey, DateTime, Date
from datetime import datetime
from db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(DECIMAL, nullable=False)
    raw_description = Column(Text, nullable=False)
    raw_category = Column(String)
    agent_category = Column(String)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String, nullable=False)
    amount = Column(DECIMAL, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Conversation(Base):
    __tablename__ = "conversation_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    specialists_called = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)