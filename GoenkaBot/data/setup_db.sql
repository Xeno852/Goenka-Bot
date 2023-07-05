CREATE TABLE IF NOT EXISTS user_stats (
    user_id TEXT PRIMARY KEY,
    streak INTEGER DEFAULT 0,
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
