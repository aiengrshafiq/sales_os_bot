# db/init_db.py
from db.session import engine
from db.models import Base

def init_database():
    """Creates all database tables based on the defined models."""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"An error occurred while creating tables: {e}")

if __name__ == "__main__":
    init_database()