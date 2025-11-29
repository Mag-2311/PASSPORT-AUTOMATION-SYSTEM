import sqlite3

conn = sqlite3.connect("database.db")  # Make sure this file exists in your folder
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

if rows:
    print("✅ Users found in database:")
    for row in rows:
        print(row)
else:
    print("❌ No users found in database!")

conn.close()
