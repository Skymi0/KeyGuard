
import sqlite3
from datetime import datetime

# Database name
DB_NAME = 'key_guard.db'

# Function to create the database
def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            share_threshold INTEGER,
            num_shares INTEGER,
            nickname TEXT,
            directory TEXT,
            encryption_type TEXT,
            security_level TEXT,
            salt INTEGER DEFAULT 0,
            creation_date TEXT,
            last_modified TEXT,
            notes TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Function to add new data to the database
def add_key(data):
    create_database()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO keys (share_threshold, num_shares, nickname, directory,
                          encryption_type, security_level, salt, creation_date, last_modified, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["share_threshold"],
        data["num_shares"],
        data["nickname"],
        data["directory"],
        data["encryption_type"],
        data["security_level"], 
        data["salt"],  # Include salt in the insertion
        data["creation_date"],
        data["last_modified"],
        data["notes"]
    ))
    
    conn.commit()
    conn.close()

# Function to retrieve keys from the database
def get_keys(reset=False):
    create_database()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM keys')
    rows = cursor.fetchall()
    
    keys = []
    for row in rows:
        keys.append({
            "id": row[0],
            "share_threshold": row[1],
            "num_shares": row[2],
            "nickname": row[3],
            "directory": row[4],
            "encryption_type": row[5],
            "security_level": row[6],
            "salt": row[7],  
            "notes": row[8]
        })
    
    
    # If no keys are found or a reset is requested
    if not keys or reset:
        if reset:
            print("Database is being reset...")
            # Add logic to reset the database here, like clearing or dropping tables.
            delete_key("1")
            conn.commit()  # Commit the changes to the database.

            print("Database is being reset and fixed...")

        elif not keys:
            print("Database is being added...")
            print("Reset App Please")
        
        # Adding data to the database if reset or no keys were found
        data = {
            "share_threshold": 3,
            "num_shares": 5,
            "nickname": "keyguard",
            "directory": "room",
            "encryption_type": "AES256",
            "security_level": "High",
            "salt": 1,  
            "creation_date": "2024-11-07",
            "last_modified": "2024-11-07",
            "notes": "This is a secure keyguard account."
        }
        add_key(data)
    conn.close()
    return keys

# Function to update fields in the 'keys' table for a specific key
def update_key(key_id, **kwargs):
    create_database()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    fields = ["share_threshold", "num_shares", "nickname", "directory", "encryption_type", "security_level", "salt", "notes"]
    if "share_threshold" in kwargs:
        kwargs["share_threshold"] = int(kwargs["share_threshold"])
    if "num_shares" in kwargs:
        kwargs["num_shares"] = int(kwargs["num_shares"])
    set_clause = ", ".join([f"{field} = ?" for field in fields if field in kwargs])
    if not set_clause:
        print("No fields to update.")
        return

    kwargs["last_modified"] = datetime.now().isoformat()
    kwargs["key_id"] = key_id
    
    try:
        cursor.execute(f'''
            UPDATE keys
            SET {set_clause}, last_modified = ?
            WHERE id = ?
        ''', tuple(kwargs[field] for field in fields if field in kwargs) + (kwargs["last_modified"], key_id))
        conn.commit()
    except Exception as e:
        print(f"Error updating key: {str(e)}")


    conn.commit()
    conn.close()

# Function to delete a key from the database
def delete_key(key_id):
    create_database()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM keys WHERE id = ?', (key_id,))
    conn.commit()
    conn.close()


