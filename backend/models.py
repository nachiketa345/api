from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from backend.db import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    f_name=Column(String,nullable=False)
    l_name=Column(String,nullable=False)
    email=Column(String,unique=True,index=True,nullable=False)
    mpin = Column(String, index=True,nullable=False)
    password = Column(String,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)
    accounts=relationship("Account",back_populates="user")
    

class Account(Base):
    __tablename__="accounts"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    account_number=Column(String(14),nullable=False,unique=True,index=True)
    balance=Column(Integer,default=0)
    account_type=Column(String)
    mobile_number=Column(String(10),nullable=False)
    aadhar_number=Column(String(12),nullable=False)
    address=Column(String,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)
    user=relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")


class Transaction(Base):
    __tablename__="transactions"
    id=Column(Integer,primary_key=True,index=True)
    account_id=Column(Integer,ForeignKey("accounts.id"))
    amount=Column(Float)
    transaction_type=Column(String)
    timestamp=Column(DateTime,default=datetime.utcnow)
    description=Column(String)
    account=relationship("Account",back_populates="transactions")




# Create tables in the database

if __name__=='__main__':
    from backend.db import engine
    Base.metadata.create_all(bind=engine)
