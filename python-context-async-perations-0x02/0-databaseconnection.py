#!/usr/bin/env python3
import sqlite3


class DatabaseConnection:
    """Custom class-based context manager for handling DB connections."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open database connection."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure connection is closed."""
        if self.conn:
            self.conn.close()
        # Returning False ensures exceptions (if any) propagate
        return False


# Example usage
if __name__ == "__main__":
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
