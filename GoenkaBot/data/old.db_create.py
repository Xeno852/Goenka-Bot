import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('meditation_bot.db')
cursor = conn.cursor()

# Create table for user_stats if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS user_stats (
                    user_id INTEGER PRIMARY KEY,
                    streak INTEGER,
                    total_time INTEGER,
                    average_time REAL)''')

# Create table for session_history if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS session_history (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    timestamp TEXT,
                    duration INTEGER,
                    FOREIGN KEY (user_id) REFERENCES user_stats(user_id))''')

# Create trigger for total_time if it doesn't exist
cursor.execute('''
CREATE TRIGGER IF NOT EXISTS update_total_time
AFTER INSERT ON session_history
BEGIN
    UPDATE user_stats
    SET total_time = total_time + NEW.duration
    WHERE user_id = NEW.user_id;
END;
''')

# Create trigger for average_time if it doesn't exist
cursor.execute('''
CREATE TRIGGER IF NOT EXISTS update_average_time
AFTER INSERT ON session_history
BEGIN
    UPDATE user_stats
    SET average_time = (SELECT total_time / COUNT(*) FROM session_history WHERE user_id = NEW.user_id)
    WHERE user_id = NEW.user_id;
END;
''')

# Commit changes and close the connection
conn.commit()
conn.close()
