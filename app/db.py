import os
import psycopg2

def db_conection(isolation):
    conn = psycopg2.connect(
    host = os.getenv("DB_HOST", "localhost"),
    port = os.getenv("DB_PORT", "5432"),
    user = os.getenv("DB_USER", "user"),
    password = os.getenv("DB_PASSWORD", "password"),
    dbname = os.getenv("DB_NAME", "el_trebol")
    )
    conn.set_isolation_level(isolation)
    return conn
