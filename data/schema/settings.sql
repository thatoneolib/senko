/* Schema file for settings tables. */

/* Guild Settings */
CREATE TABLE IF NOT EXISTS "guild_settings" (
    "guild" BIGINT NOT NULL,
    "prefix" VARCHAR(10),
    "locale" TEXT,
    "timezone" TEXT,
    "first_joined" TIMESTAMPTZ DEFAULT (NOW() AT TIME ZONE 'UTC'),
    "last_joined" TIMESTAMPTZ DEFAULT (NOW() AT TIME ZONE 'UTC'),
    CONSTRAINT pk_guild_settings PRIMARY KEY ("guild")
);
