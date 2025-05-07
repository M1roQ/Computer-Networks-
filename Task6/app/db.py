import os

import psycopg2

def get_db():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    return conn, cursor
