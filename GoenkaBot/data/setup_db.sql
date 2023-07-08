-- DROP TABLE IF EXISTS user_stats;
-- DROP TABLE IF EXISTS session_history;
-- -- Uncomment the above lines to reset the database

CREATE TABLE IF NOT EXISTS user_stats (
    user_id TEXT PRIMARY KEY,
    total_sessions INTEGER DEFAULT 0,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_meditation_date TEXT,
    total_time INTEGER DEFAULT 0,
    average_time REAL DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS session_history (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    duration INTEGER,
    start_members TEXT,
    end_members TEXT,
    completed_members TEXT
);
