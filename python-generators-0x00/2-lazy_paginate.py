#!/usr/bin/env python3
"""
Lazy pagination over user_data.
- lazy_pagination(page_size): generator yielding pages (lists of dicts)
- includes paginate_users(page_size, offset)
"""

from seed import connect_to_prodev, TABLE_NAME

def paginate_users(page_size, offset):
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(f"SELECT * FROM {TABLE_NAME} LIMIT %s OFFSET %s", (page_size, offset))
        rows = cursor.fetchall()
        # normalize ages to int when integral for matching sample output
        for r in rows:
            try:
                r["age"] = int(r["age"])
            except Exception:
                pass
        return rows
    finally:
        cursor.close()
        connection.close()

def lazy_pagination(page_size):
    """Single-loop lazy paginator that fetches the next page only when needed."""
    if page_size <= 0:
        raise ValueError("page_size must be > 0")
    offset = 0
    while True:  # one loop total
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
