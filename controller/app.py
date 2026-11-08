import re
from model import crud
from model.errors import DbError
from model.tables import TABLES
from controller.inputs import parse
from view import console as v

PAGE_SIZE = 20
_YES = ("так", "т", "yes", "y")


def read_values(cfg, partial=False):
    values = {}
    for col, label, kind, required in cfg["fields"]:
        if partial:
            label = re.sub(r"\(Enter[^)]*\)", "(Enter - без змін)", label)
        text = v.ask(f"{label}: ")
        if text == "":
            if kind == "bool" and not partial:
                values[col] = False
                continue
            if required and not partial:
                raise ValueError(f"поле «{col}» не може бути порожнім")
            continue
        values[col] = parse(kind, text)
    return values


def show_page(conn, cfg):
    page = 0
    while True:
        cols, rows = crud.list_rows(conn, cfg, PAGE_SIZE, page * PAGE_SIZE)
        v.show_table(cols, rows)
        if len(rows) < PAGE_SIZE:
            return
        if v.ask("Enter - наступна сторінка, 0 - вийти: ") == "0":
            return
        page += 1


def delete_flow(conn, cfg):
    """Вилучення із показом залежних записів (referential action у БД)."""
    row_id = parse("uuid", v.ask("ID запису: "))
    deps = crud.count_dependents(conn, cfg, row_id)
    total = sum(n for _, n in deps)
    if total:
        v.message("Із цим записом пов'язані (зовнішні ключі):")
        for label, n in deps:
            v.message(f"  - {label}: {n}")
        if v.ask("Підтвердити вилучення? (так/ні): ").lower() not in _YES:
            v.message("Вилучення скасовано.")
            return
    affected = crud.delete_row(conn, cfg, row_id)
    if not affected:
        v.message("Запис з таким id не знайдено.")
    elif total:
        v.message(f"Видалено. Разом із ним каскадно вилучено пов'язаних записів: {total}.")
    else:
        v.message("Видалено.")


def table_loop(conn, cfg):
    while True:
        choice = v.table_menu(cfg["name"])
        try:
            if choice == "1":
                show_page(conn, cfg)
            elif choice == "2":
                values = read_values(cfg)
                new_id = crud.insert_row(conn, cfg, values)
                v.message(f"Додано, id = {new_id}")
            elif choice == "3":
                row_id = parse("uuid", v.ask("ID запису: "))
                v.message("Введіть нові значення (Enter - залишити без змін):")
                values = read_values(cfg, partial=True)
                if not values:
                    v.message("Нічого не змінено.")
                    continue
                n = crud.update_row(conn, cfg, row_id, values)
                v.message("Оновлено." if n else "Запис з таким id не знайдено.")
            elif choice == "4":
                delete_flow(conn, cfg)
            elif choice == "0":
                return
            else:
                v.message("Невідомий пункт меню.")
        except ValueError as e:
            v.message(f"Помилка введення: {e}")
        except DbError as e:
            v.message(f"Помилка: {e}")


def run(conn):
    while True:
        choice = v.main_menu(TABLES)
        if choice in TABLES:
            table_loop(conn, TABLES[choice])
        elif choice == "0":
            return
        else:
            v.message("Невідомий пункт меню.")