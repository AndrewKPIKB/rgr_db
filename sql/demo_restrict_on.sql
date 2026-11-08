SET search_path TO "LABA_1_FINAL";

BEGIN;
ALTER TABLE "Like" DROP CONSTRAINT like_from_fk;
ALTER TABLE "Like" DROP CONSTRAINT like_to_fk;
ALTER TABLE "Like"
    ADD CONSTRAINT like_from_fk FOREIGN KEY (user_id_from)
        REFERENCES "User" (user_id) ON UPDATE NO ACTION ON DELETE RESTRICT;
ALTER TABLE "Like"
    ADD CONSTRAINT like_to_fk FOREIGN KEY (user_id_to)
        REFERENCES "User" (user_id) ON UPDATE NO ACTION ON DELETE RESTRICT;
COMMIT;

-- Перевірка: confdeltype = 'r' (restrict) для like_from_fk та like_to_fk
SELECT conname, confdeltype FROM pg_constraint
WHERE connamespace = '"LABA_1_FINAL"'::regnamespace AND contype = 'f'
ORDER BY conname;