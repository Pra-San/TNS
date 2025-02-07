import pandas as pd
import sqlite3
import json


def create_connection(db_file='scheduled_populator/news_headlines.db'):
    # Create a SQLite database (or connect if it exists)
    conn = sqlite3.connect(db_file)
    create_news_headlines_table(conn)
    return conn


def close_connection(conn):
    conn.close()

def create_news_headlines_table(conn):
    create_table_query = """
        CREATE TABLE IF NOT EXISTS news_headlines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        headline TEXT,
        url TEXT,
        headline_sentiment TEXT,
        sector_tags TEXT
    );
    """
    conn.execute(create_table_query)
    conn.commit()


def get_existing_headlines():
    conn = create_connection()
    try:
        existing_news_df = pd.read_sql_query("SELECT * FROM news_headlines", conn)
        existing_news_df['sector_tags'] = existing_news_df['sector_tags'].apply(lambda x: json.loads(x))
    except pd.io.sql.DatabaseError as e:
        print(f"Error fetching headlines: {e}")
        existing_news_df = pd.DataFrame()
    close_connection(conn)
    return existing_news_df


def save_headlines(processed_headlines_df):
    # Convert sector_tags list to JSON strings before saving to DB
    processed_headlines_df['sector_tags'] = processed_headlines_df['sector_tags'].apply(lambda x: json.dumps(x))

    conn = create_connection()
    processed_headlines_df.to_sql('news_headlines', conn, if_exists='append', index=False)
    close_connection(conn)

