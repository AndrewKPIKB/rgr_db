from model import generator
from model.errors import DbError
from controller.inputs import read_positive_int
from view import console as v


def run(conn):
    while True:
        choice = v.generation_menu()
        try:
            if choice in generator.GENERATORS:
                n = read_positive_int("Кількість записів")
                rows, ms = generator.generate(conn, choice, n)
                v.message(f"Додано записів: {rows}. Час виконання: {ms:.1f} мс")
            elif choice == "5":
                n = read_positive_int("Кількість користувачів (і лайків)")
                for name, rows, ms in generator.generate_all(conn, n):
                    v.message(f"{name}: додано {rows} записів за {ms:.1f} мс")
            elif choice == "0":
                return
            else:
                v.message("Невідомий пункт меню.")
        except ValueError as e:
            v.message(f"Помилка введення: {e}")
        except DbError as e:
            v.message(f"Помилка: {e}")