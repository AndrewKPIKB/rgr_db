from psycopg import sql
from model.errors import DbError, translate


def _execute(conn, query, params=(), op="", fetch=False):
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            result = None
            if fetch:
                cols = [d.name for d in cur.description]
                result = (cols, cur.fetchall())
            affected = cur.rowcount
        conn.commit()
        return result, affected
    except Exception as e:
        conn.rollback()
        raise DbError(translate(e, op)) from e


def list_rows(conn, cfg, limit, offset):
    query = sql.SQL("SELECT * FROM {t} ORDER BY {pk} LIMIT %s OFFSET %s").format(
        t=sql.Identifier(cfg["table"]), pk=sql.Identifier(cfg["pk"]))
    result, _ = _execute(conn, query, (limit, offset), op="select", fetch=True)
    return result


def insert_row(conn, cfg, values: dict):
    query = sql.SQL("INSERT INTO {t} ({cols}) VALUES ({ph}) RETURNING {pk}").format(
        t=sql.Identifier(cfg["table"]),
        cols=sql.SQL(", ").join(sql.Identifier(c) for c in values),
        ph=sql.SQL(", ").join(sql.Placeholder() for _ in values),
        pk=sql.Identifier(cfg["pk"]))
    result, _ = _execute(conn, query, list(values.values()), op="insert", fetch=True)
    return result[1][0][0]


def update_row(conn, cfg, row_id, values: dict):
    query = sql.SQL("UPDATE {t} SET {sets} WHERE {pk} = %s").format(
        t=sql.Identifier(cfg["table"]),
        sets=sql.SQL(", ").join(
            sql.SQL("{} = %s").format(sql.Identifier(c)) for c in values),
        pk=sql.Identifier(cfg["pk"]))
    _, affected = _execute(conn, query, list(values.values()) + [row_id], op="update")
    return affected


def delete_row(conn, cfg, row_id):
    query = sql.SQL("DELETE FROM {t} WHERE {pk} = %s").format(
        t=sql.Identifier(cfg["table"]), pk=sql.Identifier(cfg["pk"]))
    _, affected = _execute(conn, query, (row_id,), op="delete")
    return affected


def count_dependents(conn, cfg, row_id):
    """Кількість залежних записів, що пов'язані із записом зовнішніми ключами.

    Повертає список (підпис, кількість). Для таблиць без залежних записів - порожній.
    """
    result = []
    for label, table, column in cfg.get("children", []):
        query = sql.SQL("SELECT count(*) FROM {t} WHERE {c} = %s").format(
            t=sql.Identifier(table), c=sql.Identifier(column))
        res, _ = _execute(conn, query, (row_id,), op="select", fetch=True)
        result.append((label, res[1][0][0]))
    return result