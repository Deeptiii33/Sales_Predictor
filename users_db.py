import sqlite3
import bcrypt

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create table for users
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Insert sample users (for testing purposes)
users = [
    ('admin', bcrypt.hashpw('admin_password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')),
    ('user', bcrypt.hashpw('user_password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
]

# Insert sample data into the users table
c.executemany('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', users)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully, and users inserted.")
