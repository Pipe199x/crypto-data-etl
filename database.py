from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

class Database:
    _instance = None  # Create a class attribute to store the database instance

    @classmethod
    def get_instance(cls) -> Client:
        # If no instance exists, create one using Supabase credentials
        if cls._instance is None:
            cls._instance = create_client(SUPABASE_URL, SUPABASE_KEY)
        return cls._instance  # Return the existing or newly created instance

# Function to get the database instance
def get_db():
    return Database.get_instance()
