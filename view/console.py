def ask(prompt: str) -> str:
    return input(prompt).strip()


def message(text: str) -> None:
    print(text)


# ---------- пункт 1: CRUD ----------
def main_menu(tables: dict) -> str:
    print("\n===== ГОЛОВНЕ МЕНЮ =====")
    for key, cfg in tables.items():
        print(f"{key}. {cfg['name']}")
    print("0. Назад до вибору пункту")
    return ask("Ваш вибір: ")


def table_menu(title: str) -> str:
    print(f"\n--- {title} ---")
    print("1. Переглянути")
    print("2. Додати")
    print("3. Редагувати")
    print("4. Видалити")
    print("0. Назад")
    return ask("Ваш вибір: ")


def show_table(cols, rows) -> None:
    if not rows:
        print("Записів немає.")
        return
    widths = [max(len(str(c)), *(len(str(r[i])) for r in rows))
              for i, c in enumerate(cols)]
    line = " | ".join(str(c).ljust(w) for c, w in zip(cols, widths))
    print(line)
    print("-" * len(line))
    for r in rows:
        print(" | ".join(str(v).ljust(w) for v, w in zip(r, widths)))


# ---------- вибір пункту завдання ----------
def task_menu() -> str:
    print("\n===== РГР: ОБЕРІТЬ ПУНКТ ЗАВДАННЯ =====")
    print("1. Пункт 1 - перегляд, внесення, редагування, вилучення даних")
    print("2. Пункт 2 - генерація даних (SQL)")
    print("3. Пункт 3 - пошук (параметризовані запити)")
    print("0. Вихід")
    return ask("Ваш вибір: ")


# ---------- пункт 2: генерація ----------
def generation_menu() -> str:
    print("\n--- Генерація даних (SQL) ---")
    print("1. Користувачі")
    print("2. Профілі (для користувачів без профілю)")
    print("3. Налаштування (для користувачів без налаштувань)")
    print("4. Лайки (випадкові пари користувачів)")
    print("5. Повний набір (усі чотири таблиці)")
    print("0. Назад")
    return ask("Ваш вибір: ")


# ---------- пункт 3: пошук ----------
def search_menu() -> str:
    print("\n--- Пошук ---")
    print("1. Користувачі за профілем (ім'я, стать, дата народження, підтвердження)")
    print("2. Найпопулярніші користувачі за лайками (GROUP BY, діапазон кількості)")
    print("3. Підходящі кандидати за налаштуваннями користувача")
    print("4. Користувачі за налаштуваннями (бажана стать, діапазони віку)")
    print("0. Назад")
    return ask("Ваш вибір: ")