
TABLES = {
    "1": {
        "name": "Користувачі (User)",
        "table": "User",
        "pk": "user_id",
        "fields": [
            ("email", "Email", "str", True),
            ("password_hash", "Хеш пароля", "str", True),
            ("phone_number", "Телефон", "str", True),
            ("is_verified", "Підтверджений true/false (Enter - false)", "bool", False),
            ("created_at", "Дата створення РРРР-ММ-ДД (Enter - сьогодні)", "date", False),
        ],
        "children": [
            ("профілі", "Profile", "user_id"),
            ("налаштування", "Preference", "user_id"),
            ("лайки, поставлені користувачем", "Like", "user_id_from"),
            ("лайки, отримані користувачем", "Like", "user_id_to"),
        ],
    },
    "2": {
        "name": "Профілі (Profile)",
        "table": "Profile",
        "pk": "profile_id",
        "fields": [
            ("user_id", "ID користувача (UUID)", "uuid", True),
            ("first_name", "Ім'я", "str", True),
            ("birth_date", "Дата народження РРРР-ММ-ДД", "date", True),
            ("gender", "Стать (male/female/other)", "str", True),
        ],
    },
    "3": {
        "name": "Вподобання (Preference)",
        "table": "Preference",
        "pk": "preference_id",
        "fields": [
            ("user_id", "ID користувача (UUID)", "uuid", True),
            ("target_gender", "Бажана стать (Enter - пропустити)", "str", False),
            ("min_age", "Мін. вік (Enter - пропустити)", "int", False),
            ("max_age", "Макс. вік (Enter - пропустити)", "int", False),
        ],
    },
    "4": {
        "name": "Лайки (Like)",
        "table": "Like",
        "pk": "like_id",
        "fields": [
            ("user_id_from", "ID того, хто ставить лайк (UUID)", "uuid", True),
            ("user_id_to", "ID того, кому лайк (UUID)", "uuid", True),
            ("timestamp", "Дата РРРР-ММ-ДД (Enter - сьогодні)", "date", False),
        ],
    },
}