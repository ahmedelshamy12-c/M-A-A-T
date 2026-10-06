# Opening the database and creating its tables.

import sqlite3

DATABASE_FILE = "data/data_base.db"
SCHEMA_FILE = "data/schema.sql"


def connect():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row  # lets us write user["email"]
    return connection


def create_tables():
    connection = connect()
    schema = open(SCHEMA_FILE, encoding="utf-8").read()
    connection.executescript(schema)
    connection.close()
