CREATE INDEX IF NOT EXISTS idx_profile_birth_date ON "Profile"(birth_date);
CREATE INDEX IF NOT EXISTS idx_like_timestamp ON "Like"("timestamp");
CREATE INDEX IF NOT EXISTS idx_profile_gender ON "Profile"(gender);
ANALYZE;