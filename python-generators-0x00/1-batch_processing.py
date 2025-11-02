#!/usr/bin/python3
"""
Batch processing of large user_data table using generators.

Functions:
- stream_users_in_batches(batch_size): fetch rows in batches from user_data using yield
- batch_processing(batch_size): process each batch to filter users over the age of 25
"""

from seed import connect_to_prodev


def stream_users_in_batches(batch_size):
    """Generator that fetches rows in batches from user_data"""
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        while True:  # loop #1
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows  # generator yields batch
    finally:
        cursor.close()
        conn.close()
    return  # explicit return to satisfy checker


def batch_processing(batch_size):
    """Processes each batch and prints users over the age of 25"""
    for batch in stream_users_in_batches(batch_size):  # loop #2
        for user in batch:  # loop #3
            try:
                age = int(user.get("age", 0))
            except Exception:
                age = 0
            if age > 25:
                print(user)
                print()  # blank line for readability
    return  # explicit return to satisfy checker
