#!/usr/bin/env python3
import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    """Handle DB connections automatically."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def cache_query(func):
    """Decorator to cache query results."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get("query")
        if query in query_cache:
            print("[CACHE HIT] Returning cached results.")
            return query_cache[query]
        print("[CACHE MISS] Executing query and caching result.")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    q = "SELECT * FROM users"
    print(fetch_users_with_cache(query=q))   # Executes and caches
    print(fetch_users_with_cache(query=q))   # Uses cache
