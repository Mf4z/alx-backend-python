#!/usr/bin/env python3
import sqlite3
import functools
from datetime import datetime   # required for timestamp logging


def log_queries(func):
    """Decorator that logs SQL queries before execution, with timestamp."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if query:
            print(f"[{timestamp}] Executing SQL query: {query}")
        else:
            print(f"[{timestamp}] Executing database operation (no query provided)")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
