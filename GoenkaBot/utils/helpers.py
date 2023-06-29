import sqlite3

def initialize_db():
    connection = sqlite3.connect("data/database.sqlite")
    cursor = connection.cursor()
    
    # Create the table for user streaks if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS streaks (user_id INTEGER PRIMARY KEY, streak_count INTEGER)''')
    
    connection.commit()
    connection.close()
