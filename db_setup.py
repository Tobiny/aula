import os
import sqlite3

# Create instance directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)

# Database file path
DB_PATH = os.path.join(INSTANCE_DIR, 'smart_classroom.db')

# Create and initialize the database directly with SQLite
def init_db():
    # Check if database already exists
    if os.path.exists(DB_PATH):
        print(f"Database already exists at {DB_PATH}")
        return
    
    print(f"Creating new database at {DB_PATH}")
    
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create classes table
    c.execute('''
    CREATE TABLE classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id TEXT,
        subject TEXT,
        date TIMESTAMP
    )
    ''')
    
    # Create readings table
    c.execute('''
    CREATE TABLE readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER,
        timestamp TIMESTAMP,
        emotion TEXT,
        FOREIGN KEY (class_id) REFERENCES classes (id)
    )
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database schema created successfully")

if __name__ == "__main__":
    init_db()
    print(f"Database setup complete. Path: {DB_PATH}")