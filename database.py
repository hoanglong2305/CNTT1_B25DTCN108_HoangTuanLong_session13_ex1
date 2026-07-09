from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

url_database = "mysql+pymysql://root:123456@localhost:3306/menu_db"

engine = create_engine(url_database)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()