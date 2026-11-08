SET search_path TO "LABA_1_FINAL";

-- 1. Кількість записів
SELECT 'User' AS table_name, count(*) AS rows_count FROM "User"
UNION ALL SELECT 'Profile', count(*) FROM "Profile"
UNION ALL SELECT 'Preference', count(*) FROM "Preference"
UNION ALL SELECT 'Like', count(*) FROM "Like";

-- 2. Порушення обмежень (усі значення мають дорівнювати 0)
SELECT 'профілі без користувача' AS check_name, count(*) AS violations
FROM "Profile" p LEFT JOIN "User" u ON u.user_id = p.user_id WHERE u.user_id IS NULL
UNION ALL
SELECT 'налаштування без користувача', count(*)
FROM "Preference" p LEFT JOIN "User" u ON u.user_id = p.user_id WHERE u.user_id IS NULL
UNION ALL
SELECT 'лайки з неіснуючим відправником', count(*)
FROM "Like" l LEFT JOIN "User" u ON u.user_id = l.user_id_from WHERE u.user_id IS NULL
UNION ALL
SELECT 'лайки з неіснуючим отримувачем', count(*)
FROM "Like" l LEFT JOIN "User" u ON u.user_id = l.user_id_to WHERE u.user_id IS NULL
UNION ALL
SELECT 'лайки самому собі', count(*) FROM "Like" WHERE user_id_from = user_id_to
UNION ALL
SELECT 'min_age > max_age', count(*) FROM "Preference" WHERE min_age > max_age
UNION ALL
SELECT 'дублікати email', count(*)
FROM (SELECT email FROM "User" GROUP BY email HAVING count(*) > 1) t
UNION ALL
SELECT 'дублікати телефонів', count(*)
FROM (SELECT phone_number FROM "User" GROUP BY phone_number HAVING count(*) > 1) t
UNION ALL
SELECT 'дублікати лайків', count(*)
FROM (SELECT 1 FROM "Like" GROUP BY user_id_from, user_id_to HAVING count(*) > 1) t;

-- 3. Розподіл булевого поля is_verified
SELECT is_verified, count(*) FROM "User" GROUP BY is_verified ORDER BY is_verified;