from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import os
import time

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://fooduser:foodpass@localhost:3306/food_recommender"
)

# Retry connection logic
max_retries = 10
retry_count = 0
engine = None

while retry_count < max_retries:
    try:
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 5}
        )
        # Test connection
        with engine.connect() as conn:
            print("✓ Successfully connected to database")
        break
    except Exception as e:
        retry_count += 1
        if retry_count < max_retries:
            print(f"⚠ Database connection failed, retrying ({retry_count}/{max_retries})...")
            time.sleep(2)
        else:
            print(f"✗ Failed to connect after {max_retries} attempts")
            raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
