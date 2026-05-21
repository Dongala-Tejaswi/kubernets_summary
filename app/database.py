from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import time

DATABASE_URL = "mysql+pymysql://root:@db:3306/notes"

# Retry DB connection
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        print("Database connected!")
        connection.close()
        break
    except Exception as e:
        print("Database not ready, retrying...")
        time.sleep(5)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()