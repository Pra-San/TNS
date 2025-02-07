CREATE TABLE IF NOT EXISTS news_headlines (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      source TEXT,
      headline TEXT,
      url TEXT,
      headline_sentiment TEXT,
      sector_tags TEXT
);