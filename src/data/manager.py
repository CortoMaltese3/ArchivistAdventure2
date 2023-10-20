import sys
import sqlite3
from pathlib import Path

from src.settings import paths


class DatabaseManager:
    def __init__(self):
        if self.is_packaged():
            directory = Path.home() / "ArchivistAdventure2"
            self.ensure_directory_exists(directory)
            self.db_path = directory / "archivist_adventure_2.db"
            self.ensure_database_exists()
        else:
            directory = paths.BASE_PATH
            self.db_path = directory / "archivist_adventure_2.db"
            self.ensure_database_exists()

    @staticmethod
    def is_packaged():
        """Check if the application is bundled using PyInstaller."""
        return getattr(sys, "frozen", False)

    @staticmethod
    def ensure_directory_exists(directory):
        """Ensure the given directory exists, and if not, create it."""
        directory.mkdir(parents=True, exist_ok=True)

    def ensure_database_exists(self):
        """Ensure the database file exists."""
        if not self.db_path.exists():
            self.init_database()

    def init_database(self):
        """Initialize the database with necessary tables and schema."""
        with self.connect() as conn:
            # Example table creation, modify as needed
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS example (
                    id INTEGER PRIMARY KEY,
                    data TEXT
                )
            """
            )
            conn.commit()

    def connect(self):
        """Open a new database connection."""
        return sqlite3.connect(self.db_path)

    def execute_query(self, query, parameters=()):
        """Execute a single query."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            conn.commit()
            return cursor

    def table_exists(self, table_name):
        """Check if a table exists in the database."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?
            """,
                (table_name,),
            )
            return cursor.fetchone()[0] == 1

    def get_data(self, table_name):
        """Fetch data from a table."""
        if not self.table_exists(table_name):
            raise ValueError(f"Table {table_name} does not exist in the database.")

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            # Convert rows to dictionary for consistency
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]