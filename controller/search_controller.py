from model import search
from model.errors import DbError
from controller.inputs import read_optional
from view import console as v


def _like(text):
    """Якщо шаблон без % та _, шукаємо входження підрядка."""
    if text is None:
        return None
    return text if ("%" in text or "_" in text) else f"%{text}%"


def _check_range(low, high, what):
    if low is not None and high is not None and low > high:
        raise ValueError(f"межа «від» для {what} більша за межу «до»")


def run(conn):
    while True:
        choice = v.search_menu()
        try:
            if choice == "0":
                return
            if choice == "1":
                name = _like(read_optional("Ім'я (шаблон, напр. An%)"))
                gender = read_optional("Стать (male/female/other)")
                b_from = read_optional("Дата народження від (РРРР-ММ-ДД)", "date")
                b_to = read_optional("Дата народження до (РРРР-ММ-ДД)", "date")
                verified = read_optional("Підтверджений (true/false)", "bool")
                cols, rows, ms = search.profiles(conn, name, gender, b_from, b_to, verified)
            elif choice == "2":
                d_from = read_optional("Лайки з дати (РРРР-ММ-ДД)", "date")
                d_to = read_optional("Лайки до дати (РРРР-ММ-ДД)", "date")
                name = _like(read_optional("Ім'я (шаблон)"))
                min_likes = read_optional("Мінімум лайків", "int") or 1
                max_likes = read_optional("Максимум лайків", "int")
                if max_likes is not None and max_likes < min_likes:
                    raise ValueError("максимум не може бути меншим за мінімум")
                cols, rows, ms = search.top_liked(conn, d_from, d_to, name,
                                                  min_likes, max_likes)
            elif choice == "3":
                email = read_optional("Email користувача")
                if email is None:
                    raise ValueError("потрібно вказати email")
                name = _like(read_optional("Ім'я кандидата (шаблон)"))
                cols, rows, ms = search.candidates(conn, email, name)
            elif choice == "4":
                target = read_optional("Бажана стать (male/female/other)")
                min_from = read_optional("Мін. вік у налаштуваннях від", "int")
                min_to = read_optional("Мін. вік у налаштуваннях до", "int")
                max_from = read_optional("Макс. вік у налаштуваннях від", "int")
                max_to = read_optional("Макс. вік у налаштуваннях до", "int")
                name = _like(read_optional("Ім'я (шаблон)"))
                _check_range(min_from, min_to, "мінімального віку")
                _check_range(max_from, max_to, "максимального віку")
                cols, rows, ms = search.preferences(conn, target, min_from, min_to,
                                                    max_from, max_to, name)
            else:
                v.message("Невідомий пункт меню.")
                continue
            v.show_table(cols, rows)
            v.message(f"Рядків: {len(rows)} (не більше {search.LIMIT}). "
                      f"Час виконання: {ms:.2f} мс")
        except ValueError as e:
            v.message(f"Помилка введення: {e}")
        except DbError as e:
            v.message(f"Помилка: {e}")