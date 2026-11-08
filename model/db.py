import os
import psycopg
from psycopg import sql
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    schema = os.getenv("DB_SCHEMA", "public")
    conn.execute(sql.SQL("SET search_path TO {}").format(sql.Identifier(schema)))
    conn.commit()
    return conn