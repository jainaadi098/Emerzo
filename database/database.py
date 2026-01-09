from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#  MERGED DECISION: Hum 'emerzo.db' hi use karenge (jisme Bhopal data hai)

SQLALCHEMY_DATABASE_URL = "sqlite:///./Emerzo.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#  IMPORTANT: Ye function API ko database session deta hai
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()