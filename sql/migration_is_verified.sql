SET search_path TO "LABA_1_FINAL";

ALTER TABLE "User"
    ADD COLUMN IF NOT EXISTS is_verified boolean NOT NULL DEFAULT false;

-- заповнюємо існуючі записи: близько 30 % підтверджених
UPDATE "User" SET is_verified = (random() < 0.3);

ANALYZE "User";