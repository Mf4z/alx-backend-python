#!/usr/bin/env python3
"""
Memory-efficient average age:
- stream_user_ages(): yields ages one-by-one (loop #1)
- main aggregation loop computes average without loading all rows (loop #2)

Output format:
  Average age of users: <value>
"""

from seed import connect_to_prodev, TABLE_NAME

def stream_user_ages():
    """Yield ages one by one from MySQL."""
    conn = connect_to_prodev()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT age FROM {TABLE_NAME}")
        for (age,) in cur:  # loop #1
            # cur returns Decimal for DECIMAL column; cast to float or int
            try:
                age_val = int(age)
            except Exception:
                age_val = float(age)
            yield age_val
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    total = 0.0
    count = 0
    for a in stream_user_ages():  # loop #2
        total += float(a)
        count += 1
    avg = (total / count) if count else 0.0
    # match exact print spec
    print(f"Average age of users: {avg}")
