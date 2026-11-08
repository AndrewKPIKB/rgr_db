import time
from model.errors import DbError, translate

LIMIT = 50

Q_PROFILES = '''
SELECT u.email, p.first_name, p.gender, p.birth_date, u.is_verified, u.created_at
FROM "User" u
JOIN "Profile" p ON p.user_id = u.user_id
WHERE (%(name)s::text IS NULL OR p.first_name ILIKE %(name)s)
  AND (%(gender)s::text IS NULL OR p.gender = %(gender)s)
  AND (%(born_from)s::date IS NULL OR p.birth_date >= %(born_from)s)
  AND (%(born_to)s::date IS NULL OR p.birth_date <= %(born_to)s)
  AND (%(verified)s::boolean IS NULL OR u.is_verified = %(verified)s)
ORDER BY p.birth_date, u.email
LIMIT %(lim)s
'''

Q_TOP_LIKED = '''
SELECT p.first_name, u.email, COUNT(*) AS likes_received
FROM "Like" l
JOIN "User" u ON u.user_id = l.user_id_to
JOIN "Profile" p ON p.user_id = u.user_id
WHERE (%(d_from)s::date IS NULL OR l."timestamp" >= %(d_from)s)
  AND (%(d_to)s::date IS NULL OR l."timestamp" <= %(d_to)s)
  AND (%(name)s::text IS NULL OR p.first_name ILIKE %(name)s)
GROUP BY u.user_id, u.email, p.first_name
HAVING COUNT(*) >= %(min_likes)s
   AND (%(max_likes)s::int IS NULL OR COUNT(*) <= %(max_likes)s)
ORDER BY likes_received DESC, u.email
LIMIT %(lim)s
'''

Q_CANDIDATES = '''
SELECT cand.email, p.first_name, p.gender,
       EXTRACT(YEAR FROM age(p.birth_date))::int AS age
FROM "User" me
JOIN "Preference" pr ON pr.user_id = me.user_id
CROSS JOIN "Profile" p
JOIN "User" cand ON cand.user_id = p.user_id
WHERE me.email = %(email)s
  AND p.user_id <> me.user_id
  AND (pr.target_gender IS NULL OR p.gender = pr.target_gender)
  AND (pr.min_age IS NULL OR EXTRACT(YEAR FROM age(p.birth_date)) >= pr.min_age)
  AND (pr.max_age IS NULL OR EXTRACT(YEAR FROM age(p.birth_date)) <= pr.max_age)
  AND NOT EXISTS (SELECT 1 FROM "Like" l
                  WHERE l.user_id_from = me.user_id AND l.user_id_to = p.user_id)
  AND (%(name)s::text IS NULL OR p.first_name ILIKE %(name)s)
ORDER BY age, cand.email
LIMIT %(lim)s
'''

# Пошук за налаштуваннями: числові діапазони по колонках min_age та max_age
Q_PREFERENCES = '''
SELECT u.email, p.first_name, pr.target_gender, pr.min_age, pr.max_age
FROM "Preference" pr
JOIN "User" u ON u.user_id = pr.user_id
JOIN "Profile" p ON p.user_id = pr.user_id
WHERE (%(target)s::text IS NULL OR pr.target_gender = %(target)s)
  AND (%(min_from)s::int IS NULL OR pr.min_age >= %(min_from)s)
  AND (%(min_to)s::int IS NULL OR pr.min_age <= %(min_to)s)
  AND (%(max_from)s::int IS NULL OR pr.max_age >= %(max_from)s)
  AND (%(max_to)s::int IS NULL OR pr.max_age <= %(max_to)s)
  AND (%(name)s::text IS NULL OR p.first_name ILIKE %(name)s)
ORDER BY pr.min_age, pr.max_age, u.email
LIMIT %(lim)s
'''


def _run(conn, query, params):
    params["lim"] = LIMIT
    try:
        with conn.cursor() as cur:
            t = time.perf_counter()
            cur.execute(query, params)       # значення передаються окремо від SQL
            rows = cur.fetchall()
            ms = (time.perf_counter() - t) * 1000
            cols = [d.name for d in cur.description]
        conn.commit()
        return cols, rows, ms
    except Exception as e:
        conn.rollback()
        raise DbError(translate(e, "select")) from e


def profiles(conn, name, gender, born_from, born_to, verified):
    return _run(conn, Q_PROFILES, {"name": name, "gender": gender,
                                   "born_from": born_from, "born_to": born_to,
                                   "verified": verified})


def top_liked(conn, d_from, d_to, name, min_likes, max_likes):
    return _run(conn, Q_TOP_LIKED, {"d_from": d_from, "d_to": d_to, "name": name,
                                    "min_likes": min_likes, "max_likes": max_likes})


def candidates(conn, email, name):
    return _run(conn, Q_CANDIDATES, {"email": email, "name": name})


def preferences(conn, target, min_from, min_to, max_from, max_to, name):
    return _run(conn, Q_PREFERENCES, {"target": target,
                                      "min_from": min_from, "min_to": min_to,
                                      "max_from": max_from, "max_to": max_to,
                                      "name": name})