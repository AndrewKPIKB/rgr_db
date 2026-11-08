-- Схема бази даних РГР: сервіс знайомств. PostgreSQL 13+ (gen_random_uuid()).
-- Скрипт можна запускати повторно: наявні таблиці не змінюються.
CREATE SCHEMA IF NOT EXISTS "LABA_1_FINAL";
SET search_path TO "LABA_1_FINAL";

CREATE TABLE IF NOT EXISTS "User" (
    user_id       uuid         NOT NULL DEFAULT gen_random_uuid(),
    email         varchar(255) NOT NULL,
    password_hash varchar(255) NOT NULL,
    phone_number  varchar(30)  NOT NULL,
    created_at    date         NOT NULL DEFAULT CURRENT_DATE,
    is_verified   boolean      NOT NULL DEFAULT false,
    CONSTRAINT "User_pkey"   PRIMARY KEY (user_id),
    CONSTRAINT user_email_uq UNIQUE (email),
    CONSTRAINT user_phone_uq UNIQUE (phone_number),
    CONSTRAINT user_email_ck CHECK (email LIKE '%_@_%.__%')
);

CREATE TABLE IF NOT EXISTS "Profile" (
    profile_id uuid         NOT NULL DEFAULT gen_random_uuid(),
    user_id    uuid         NOT NULL,
    first_name varchar(100) NOT NULL,
    birth_date date         NOT NULL,
    gender     varchar(10)  NOT NULL,
    CONSTRAINT "Profile_pkey"        PRIMARY KEY (profile_id),
    CONSTRAINT "Profile_user_id_key" UNIQUE (user_id),
    CONSTRAINT profile_user_fk FOREIGN KEY (user_id)
        REFERENCES "User" (user_id) ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT profile_birth_ck  CHECK (birth_date > DATE '1900-01-01'),
    CONSTRAINT profile_gender_ck CHECK (gender IN ('male', 'female', 'other'))
);

CREATE TABLE IF NOT EXISTS "Preference" (
    preference_id uuid        NOT NULL DEFAULT gen_random_uuid(),
    user_id       uuid        NOT NULL,
    target_gender varchar(10),
    min_age       integer,
    max_age       integer,
    CONSTRAINT "Preference_pkey"        PRIMARY KEY (preference_id),
    CONSTRAINT "Preference_user_id_key" UNIQUE (user_id),
    CONSTRAINT preference_user_fk FOREIGN KEY (user_id)
        REFERENCES "User" (user_id) ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT pref_gender_ck  CHECK (target_gender IN ('male', 'female', 'other')),
    CONSTRAINT pref_min_age_ck CHECK (min_age >= 18),
    CONSTRAINT pref_max_age_ck CHECK (max_age <= 120),
    CONSTRAINT pref_range_ck   CHECK (min_age <= max_age)
);

CREATE TABLE IF NOT EXISTS "Like" (
    like_id      uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id_to   uuid NOT NULL,
    user_id_from uuid NOT NULL,
    "timestamp"  date NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT "Like_pkey" PRIMARY KEY (like_id),
    CONSTRAINT like_from_fk FOREIGN KEY (user_id_from)
        REFERENCES "User" (user_id) ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT like_to_fk FOREIGN KEY (user_id_to)
        REFERENCES "User" (user_id) ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT like_pair_uq UNIQUE (user_id_from, user_id_to),
    CONSTRAINT like_self_ck CHECK (user_id_from <> user_id_to)
);