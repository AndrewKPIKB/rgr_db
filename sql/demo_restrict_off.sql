SET search_path TO "LABA_1_FINAL";

BEGIN;
ALTER TABLE "Like" DROP CONSTRAINT like_from_fk;
ALTER TABLE "Like" DROP CONSTRAINT like_to_fk;
ALTER TABLE "Like"
    ADD CONSTRAINT like_from_fk FOREIGN KEY (user_id_from)
        REFERENCES "User" (user_id) ON UPDATE NO ACTION ON DELETE CASCADE;
ALTER TABLE "Like"
    ADD CONSTRAINT like_to_fk FOREIGN KEY (user_id_to)
        REFERENCES "User" (user_id) ON UPDATE NO ACTION ON DELETE CASCADE;
COMMIT;

-- Перевірка: confdeltype = 'c' (cascade) для всіх чотирьох зовнішніх ключів
SELECT conname, confdeltype FROM pg_constraint
WHERE connamespace = '"LABA_1_FINAL"'::regnamespace AND contype = 'f'
ORDER BY conname;