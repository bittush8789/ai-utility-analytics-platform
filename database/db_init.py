import os
import sys

# Add the project root to sys.path so we can import from the database package
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from database.generate_data import generate_all_data

def init_db():
    db_path = "utility_analytics.db"
    print("Starting DB initialization process...")
    generate_all_data(db_path)
    print("Database initialization process finished.")

if __name__ == "__main__":
    init_db()
