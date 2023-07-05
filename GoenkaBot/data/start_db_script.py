import sqlite3

with open("setup_db.sql", "r") as file:
    sql_script = file.read()

db_path = "meditation.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Execute the script to create tables
cursor.executescript(sql_script)

# Commit and close
conn.commit()
conn.close()
