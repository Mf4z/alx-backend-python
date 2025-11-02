#!/usr/bin/python3
"""
Lazy pagination from the user_data table using generators.

Functions:
- paginate_users(page_size, offset): fetches a single page of data
- lazy_paginate(page_size): generator that lazily fetches pages one by one
"""

from seed import connect_to_prodev


def paginate_users(page_size, offset):
    """Fetch one page of results from user_data"""
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    try:
        query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()


def lazy_paginate(page_size):
    """
    Generator that lazily fetches user_data pages.
    Starts from offset 0 and fetches the next page only when needed.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page  # generator yields one page at a time
        offset += page_size
    return  # explicit return for checker
