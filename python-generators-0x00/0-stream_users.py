#!/usr/bin/env python3
"""
Generator that streams rows one by one from MySQL.
- Uses a single loop in the generator.
- Yields dicts: {'user_id': ..., 'name': ..., 'email': ..., 'age': ...}
"""

from seed import connect_to_prodev, TABLE_NAME

def stream_users():
    """Fetch rows one by one using a generator (single loop)."""
    conn = connect_to_prodev()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(f"SELECT user_id, name, email, age FROM {TABLE_NAME}")
        # one loop; cursor is iterable row-by-row without loading all rows
        for row in cur:
            # coerce DECIMAL to int if it looks integral, to match sample output
            age = row["age"]
            try:
                age = int(age)
            except Exception:
                pass
            yield {
                "user_id": row["user_id"],
                "name": row["name"],
                "email": row["email"],
                "age": age,
            }
    finally:
        cur.close()
        conn.close()
