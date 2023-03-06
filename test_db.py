import asyncio

from db import on_startup, on_shutdown
from models import Users

async def display():
    await on_startup()
    users = await Users.all()
    for user in users:
        print(user.login)
        print([perm.perm_name for perm in await user.permissions.all()])
    await on_shutdown()


if __name__ == '__main__':
    asyncio.run(display())
