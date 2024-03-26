from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# url_object = URL.create(
#     "mysql+pymysql",
#     username="root",
#     password="mypass",  
#     host="localhost",
#     database="sandbox001",
# )

SQLALCHEMY_DATABASE_URL = os.environ['SQLALCHEMY_DATABASE_URL'] 

engine = create_engine(SQLALCHEMY_DATABASE_URL) # generates the pool 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()