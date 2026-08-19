import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Isi password Supabase kamu di sini (apa adanya, walaupun ada karakter @)
DB_USER = "postgres"
DB_PASSWORD = "@Alfifebri03" 
DB_HOST = "db.sdntsnrwmsdzvzukmfjd.supabase.co"
DB_PORT = "5432"
DB_NAME = "postgres"

# 2. Encode password agar karakter khusus seperti @ tidak merusak URL koneksi
encoded_password = quote_plus(DB_PASSWORD)

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()