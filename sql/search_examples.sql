SET search_path TO "LABA_1_FINAL";

-- Запит 1 (вимірювання): дата народження 1999-01-01 .. 1999-03-31
EXPLAIN ANALYZE
SELECT u.email, p.first_name, p.gender, p.birth_date, u.is_verified, u.created_at
FROM "User" u
JOIN "Profile" p ON p.user_id = u.user_id
WHERE p.birth_date >= DATE '1999-01-01'
  AND p.birth_date <= DATE '1999-03-31'
ORDER BY p.birth_date, u.email
LIMIT 50;

-- Запит 1 (приклад з усіма фільтрами, зокрема булевим)
EXPLAIN ANALYZE
SELECT u.email, p.first_name, p.gender, p.birth_date, u.is_verified, u.created_at
FROM "User" u
JOIN "Profile" p ON p.user_id = u.user_id
WHERE p.first_name ILIKE '%Anna%'
  AND p.gender = 'female'
  AND p.birth_date >= DATE '1990-01-01'
  AND p.birth_date <= DATE '2000-12-31'
  AND u.is_verified = true
ORDER BY p.birth_date, u.email
LIMIT 50;

-- Запит 2 (вимірювання): лайки 2026-05-01 .. 2026-06-30, мінімум лайків 1
EXPLAIN ANALYZE
SELECT p.first_name, u.email, COUNT(*) AS likes_received
FROM "Like" l
JOIN "User" u ON u.user_id = l.user_id_to
JOIN "Profile" p ON p.user_id = u.user_id
WHERE l."timestamp" >= DATE '2026-05-01'
  AND l."timestamp" <= DATE '2026-06-30'
GROUP BY u.user_id, u.email, p.first_name
HAVING COUNT(*) >= 1
ORDER BY likes_received DESC, u.email
LIMIT 50;

-- Запит 2 (приклад з діапазоном кількості лайків 2..3)
EXPLAIN ANALYZE
SELECT p.first_name, u.email, COUNT(*) AS likes_received
FROM "Like" l
JOIN "User" u ON u.user_id = l.user_id_to
JOIN "Profile" p ON p.user_id = u.user_id
WHERE l."timestamp" >= DATE '2025-01-01'
  AND l."timestamp" <= DATE '2026-06-30'
GROUP BY u.user_id, u.email, p.first_name
HAVING COUNT(*) >= 2 AND COUNT(*) <= 3
ORDER BY likes_received DESC, u.email
LIMIT 50;

-- Запит 3 (вимірювання): кандидати для user5@example.com
EXPLAIN ANALYZE
SELECT cand.email, p.first_name, p.gender,
       EXTRACT(YEAR FROM age(p.birth_date))::int AS age
FROM "User" me
JOIN "Preference" pr ON pr.user_id = me.user_id
CROSS JOIN "Profile" p
JOIN "User" cand ON cand.user_id = p.user_id
WHERE me.email = 'user5@example.com'
  AND p.user_id <> me.user_id
  AND (pr.target_gender IS NULL OR p.gender = pr.target_gender)
  AND (pr.min_age IS NULL OR EXTRACT(YEAR FROM age(p.birth_date)) >= pr.min_age)
  AND (pr.max_age IS NULL OR EXTRACT(YEAR FROM age(p.birth_date)) <= pr.max_age)
  AND NOT EXISTS (SELECT 1 FROM "Like" l
                  WHERE l.user_id_from = me.user_id AND l.user_id_to = p.user_id)
ORDER BY age, cand.email
LIMIT 50;

-- Запит 4 (приклад): налаштування з бажаною статтю female,
-- мінімальний вік 20..25, максимальний вік 30..40
EXPLAIN ANALYZE
SELECT u.email, p.first_name, pr.target_gender, pr.min_age, pr.max_age
FROM "Preference" pr
JOIN "User" u ON u.user_id = pr.user_id
JOIN "Profile" p ON p.user_id = pr.user_id
WHERE pr.target_gender = 'female'
  AND pr.min_age >= 20 AND pr.min_age <= 25
  AND pr.max_age >= 30 AND pr.max_age <= 40
ORDER BY pr.min_age, pr.max_age, u.email
LIMIT 50;