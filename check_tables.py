import sqlite3

conn = sqlite3.connect("database.db")  # Connect to the database
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("✅ Tables in database:", tables)  # Print the tables

conn.close()
