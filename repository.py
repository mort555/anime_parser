import sqlite3


class DatabaseRepository:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, timeout=30)
        self.cursor = self.conn.cursor()

    def create_anime_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS anime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT,
            image TEXT,
            episode TEXT,
            views TEXT,
            year TEXT,
            genres TEXT,
            tags TEXT
        )
        """)
    def insert_data_to_anime_table(self, data, batch_size):
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]

            self.cursor.executemany("""
            INSERT INTO anime (title, link, image, episode, views)
            VALUES (:title, :link, :image, :episode, :views)
            """, batch)

            self.conn.commit()
    def get_all_links_without_additional_info(self):
        self.cursor.execute("""
        SELECT link FROM anime
        WHERE year IS NULL OR genres IS NULL OR tags IS NULL
        """)
        
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]
    def insert_add_data_to_anime_table(self, data, batch_size):
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]

            self.cursor.executemany("""
            UPDATE anime
            SET year = :year,
                genres = :genres,
                tags = :tags
            WHERE link = :link
            """, batch)

            self.conn.commit()