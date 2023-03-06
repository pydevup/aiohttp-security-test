from tortoise import Tortoise

db = Tortoise()

async def on_startup():
    await db.init(config=TORTOISE_ORM)


async def on_shutdown():
    await db.close_connections()


POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_PASSWORD = "aiohttp_security"
POSTGRES_USER = "aiohttp_security"
POSTGRES_DB = "aiohttp_security"
POSTGRES_URI = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

TORTOISE_ORM = {
    "connections": {"default": POSTGRES_URI},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
