SET search_path TO "LABA_1_FINAL";

-- 1. Користувачі (10 штук)
WITH base AS (
    SELECT coalesce(max(substr(phone_number, 7)::int), 0) AS s
    FROM "User"
    WHERE phone_number ~ '^\+38099[0-9]{7}$'
)
INSERT INTO "User" (email, password_hash, phone_number, created_at, is_verified)
SELECT 'user' || (base.s + g.i) || '@example.com',
       md5(random()::text),
       '+38099' || lpad((base.s + g.i)::text, 7, '0'),
       DATE '2023-01-01' + floor(random() * 1300)::int,
       random() < 0.3
FROM generate_series(1, 10) AS g(i)
CROSS JOIN base;

-- 2. Профілі для користувачів без профілю (10 штук)
WITH tgt AS MATERIALIZED (
    SELECT u.user_id, row_number() OVER () AS rn
    FROM "User" u
    WHERE NOT EXISTS (SELECT 1 FROM "Profile" p WHERE p.user_id = u.user_id)
    LIMIT 10
), rnd AS MATERIALIZED (
    SELECT g.i AS rn,
           random() AS r_name, random() AS r_birth, random() AS r_gender
    FROM generate_series(1, (SELECT count(*)::int FROM tgt)) AS g(i)
)
INSERT INTO "Profile" (user_id, first_name, birth_date, gender)
SELECT t.user_id,
       (ARRAY['Anna','Ivan','Olena','Petro','Maria','Andrii','Sofiia','Taras','Iryna','Oleh'])
           [1 + floor(r.r_name * 10)::int],
       DATE '1960-01-01' + floor(r.r_birth * 17000)::int,
       (ARRAY['male','female','other'])[1 + floor(r.r_gender * 3)::int]
FROM tgt t
JOIN rnd r ON r.rn = t.rn;

-- 3. Налаштування для користувачів без налаштувань (10 штук)
WITH tgt AS MATERIALIZED (
    SELECT u.user_id, row_number() OVER () AS rn
    FROM "User" u
    WHERE NOT EXISTS (SELECT 1 FROM "Preference" p WHERE p.user_id = u.user_id)
    LIMIT 10
), rnd AS MATERIALIZED (
    SELECT g.i AS rn,
           random() AS r_gender, random() AS r_min, random() AS r_span
    FROM generate_series(1, (SELECT count(*)::int FROM tgt)) AS g(i)
)
INSERT INTO "Preference" (user_id, target_gender, min_age, max_age)
SELECT t.user_id,
       (ARRAY['male','female','other'])[1 + floor(r.r_gender * 3)::int],
       18 + floor(r.r_min * 20)::int,
       18 + floor(r.r_min * 20)::int + floor(r.r_span * 40)::int
FROM tgt t
JOIN rnd r ON r.rn = t.rn;

-- 4. Лайки (10 випадкових пар)
WITH u AS MATERIALIZED (
    SELECT user_id, row_number() OVER (ORDER BY user_id) AS rn FROM "User"
), cnt AS (
    SELECT count(*)::int AS c FROM u
), pairs AS MATERIALIZED (
    SELECT 1 + floor(random() * cnt.c)::int AS f,
           1 + floor(random() * cnt.c)::int AS t,
           DATE '2024-01-01' + floor(random() * 900)::int AS d
    FROM generate_series(1, 10) AS g(i)
    CROSS JOIN cnt
)
INSERT INTO "Like" (user_id_from, user_id_to, "timestamp")
SELECT uf.user_id, ut.user_id, p.d
FROM pairs p
JOIN u uf ON uf.rn = p.f
JOIN u ut ON ut.rn = p.t
WHERE uf.user_id <> ut.user_id
ON CONFLICT DO NOTHING;