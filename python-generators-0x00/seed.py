#!/usr/bin/env python3
"""
Seed + DB utilities for the Python Generators project.

Env vars supported (with sensible defaults for local dev):
  MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD
CSV file expected to have headers: user_id,name,email,age
"""

import csv
import os
import uuid
import mysql.connector
from mysql.connector import errorcode

DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def _mysql_config(include_db: bool = False):
    cfg = {
        "host": os.environ.get("MYSQL_HOST", "localhost"),
        "port": int(os.environ.get("MYSQL_PORT", "3306")),
        "user": os.environ.get("MYSQL_USER", "root"),
        "password": os.environ.get("MYSQL_PASSWORD", ""),
    }
    if include_db:
        cfg["database"] = DB_NAME
    return cfg

def connect_db():
    """connects to the mysql database server (no specific DB)"""
    try:
        conn = mysql.connector.connect(**_mysql_config())
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """creates the database ALX_prodev if it does not exist"""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        connection.commit()
    finally:
        cursor.close()

def connect_to_prodev():
    """connects the the ALX_prodev database in MYSQL"""
    try:
        conn = mysql.connector.connect(**_mysql_config(include_db=True))
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            root = connect_db()
            if root:
                create_database(root)
                root.close()
                return mysql.connector.connect(**_mysql_config(include_db=True))
        print(f"Error connecting to {DB_NAME}: {err}")
        return None

def create_table(connection):
    """creates a table user_data if it does not exists with the required fields"""
    # age is DECIMAL per spec; use DECIMAL(5,2) to be flexible
    DDL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5,2) NOT NULL,
        INDEX (user_id),
        INDEX (email)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    cur = connection.cursor()
    try:
        cur.execute(DDL)
        connection.commit()
        print("Table user_data created successfully")
    finally:
        cur.close()

def insert_data(connection, csv_path: str):
    """inserts data in the database if it does not exist (idempotent by user_id)"""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    cur = connection.cursor()
    try:
        sql = f"""
            INSERT INTO {TABLE_NAME} (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
              name = VALUES(name),
              email = VALUES(email),
              age = VALUES(age)
        """
        to_insert = []
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                uid = row.get("user_id") or str(uuid.uuid4())
                name = row.get("name", "").strip()
                email = row.get("email", "").strip()
                age = row.get("age")
                to_insert.append((uid, name, email, age))
        if to_insert:
            cur.executemany(sql, to_insert)
            connection.commit()
    finally:
        cur.close()
