from controller import app, generation_controller, search_controller
from view import console as v


def run(conn):
    while True:
        choice = v.task_menu()
        if choice == "1":
            app.run(conn)                    # пункт 1: наявний CRUD
        elif choice == "2":
            generation_controller.run(conn)  # пункт 2
        elif choice == "3":
            search_controller.run(conn)      # пункт 3
        elif choice == "0":
            v.message("До побачення!")
            return
        else:
            v.message("Невідомий пункт меню.")