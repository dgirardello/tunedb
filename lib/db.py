import os
import sqlite3
from lib import constants

DB_FILE_PATH = os.path.abspath(constants.DB_FILE)


def get_connection():
    return sqlite3.connect(DB_FILE_PATH)


def query_db_select(query):
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def query_db_insert(table, columns, values):
    conn   = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO {table}({columns}) VALUES({values});".format(table=table, columns=','.join(columns), values=','.join(['?'] * len(columns)))
    cursor.execute(query, values)
    conn.commit()
    return cursor.lastrowid
