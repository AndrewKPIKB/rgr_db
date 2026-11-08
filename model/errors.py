from psycopg import errors as pg


class DbError(Exception):
    """Помилка БД з повідомленням, зрозумілим користувачу."""


# повідомлення за назвою порушеного обмеження (імена задані у constraints.sql)
CONSTRAINT_MESSAGES = {
    "user_email_uq": "Користувач з таким email уже існує.",
    "user_phone_uq": "Цей номер телефону вже використовується.",
    "user_email_ck": "Некоректний формат email.",
    "Profile_user_id_key": "Для цього користувача профіль уже існує.",
    "Preference_user_id_key": "Для цього користувача вподобання вже існують.",
    "profile_gender_ck": "Стать має бути: male, female або other.",
    "profile_birth_ck": "Некоректна дата народження.",
    "pref_gender_ck": "Бажана стать має бути: male, female або other.",
    "pref_min_age_ck": "Мінімальний вік не може бути меншим за 18.",
    "pref_max_age_ck": "Максимальний вік не може перевищувати 120.",
    "pref_range_ck": "Мінімальний вік не може бути більшим за максимальний.",
    "like_pair_uq": "Такий лайк уже існує.",
    "like_self_ck": "Не можна поставити лайк самому собі.",
}


def translate(e: Exception, op: str = "") -> str:
    name = getattr(getattr(e, "diag", None), "constraint_name", None)
    if name in CONSTRAINT_MESSAGES:
        return CONSTRAINT_MESSAGES[name]

    if isinstance(e, (pg.ForeignKeyViolation, pg.RestrictViolation)):
        if op == "delete":
            return "Не можна видалити: на цей запис посилаються інші записи."
        return "Вказаного користувача не існує (порушено зовнішній ключ)."
    if isinstance(e, pg.UniqueViolation):
        return "Запис із таким унікальним значенням уже існує."
    if isinstance(e, pg.NotNullViolation):
        return "Не заповнено обов'язкове поле."
    if isinstance(e, pg.CheckViolation):
        return "Значення не відповідає обмеженню."
    if isinstance(e, (pg.InvalidTextRepresentation,
                      pg.NumericValueOutOfRange,
                      pg.InvalidDatetimeFormat,
                      pg.DatetimeFieldOverflow)):
        return "Некоректний формат або значення поза допустимим діапазоном."
    if isinstance(e, pg.StringDataRightTruncation):
        return "Текст задовгий для цього поля."
    return "Помилка бази даних. Операцію скасовано."