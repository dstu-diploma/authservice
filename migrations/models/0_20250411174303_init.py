from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "usertokens" (
        "id" SERIAL NOT NULL PRIMARY KEY,
        "user_id" INT NOT NULL,
        "token_revision" INT NOT NULL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS "aerich" (
        "id" SERIAL NOT NULL PRIMARY KEY,
        "version" VARCHAR(255) NOT NULL,
        "app" VARCHAR(100) NOT NULL,
        "content" JSONB NOT NULL
    );"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return ""
