import psycopg

from model.db import get_connection
from controller.main_controller import run


def main():
    try:
        conn = get_connection()
    except psycopg.OperationalError:
        print("Не вдалося підключитися до БД. Перевірте файл .env і чи запущений PostgreSQL.")
        return
    try:
        run(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()