from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


#connecting to the db
DATABASE_URL="postgresql+psycopg2://bank_user:Netflix%4013@localhost/bank_db"

engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

# Dependency to get database session
def get_db():
    """Provide a database session to endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
