#!/usr/bin/env python3
"""
Batch processing large data:
- stream_users_in_batches(batch_size): yields lists of row dicts using fetchmany
- batch_processing(batch_size): prints users with age > 25 (<= 3 loops total)
"""

from seed import connect_to_prodev, TABLE_NAME

def stream_users_in_batches(batch_size):
    """Yield batches (lists) of users using fetchmany(batch_size)."""
    if batch_size <= 0:
        raise ValueError("batch_size must be > 0")
    conn = connect_to_prodev()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(f"SELECT user_id, name, email, age FROM {TABLE_NAME}")
        while True:  # loop #1
            rows = cur.fetchmany(batch_size)
            if not rows:
                break
            # normalize ages to int when integral
            batch = []
            for r in rows:  # loop #2 (within allowed total <=3)
                age = r["age"]
                try:
                    age = int(age)
                except Exception:
                    pass
                r["age"] = age
                batch.append(r)
            yield batch
    finally:
        cur.close()
        conn.close()

def batch_processing(batch_size):
    """
    Processes each batch and prints only users over age 25.
    This uses at most 3 loops (outer batches, inner rows). Printing inline
    to match your 2-main.py usage (no iteration on the caller side).
    """
    for batch in stream_users_in_batches(batch_size):  # loop #3
        for user in batch:
            if (isinstance(user["age"], (int, float)) and user["age"] > 25):
                print(user)
                print()  # matches the blank line seen in your example
