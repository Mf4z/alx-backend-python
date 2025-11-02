#!/usr/bin/python3
"""
Batch processing of large user_data table using generators.
Requirements:
- stream_users_in_batches(batch_size): fetch rows from user_data in batches using yield
- batch_processing(batch_size): process each batch to filter users over age 25
- Must use <= 3 loops
"""

from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    """Generator that fetches rows in batches from user_data"""
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        while True:   # loop #1
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows   # <--- yield generator
    finally:
        cursor.close()
        conn.close()


def batch_processing(batch_size):
    """Processes each batch and prints users over the age of 25"""
    for batch in stream_users_in_batches(batch_size):  # loop #2
        for user in batch:  # loop #3
            age = int(user.get("age", 0))
            if age > 25:
                print(user)
                print()  # for readability
