from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_usertokens_user_id_05e74d" ON "usertokens" ("user_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_usertokens_user_id_05e74d";"""
