import asyncio
from typing import Tuple

from aiohttp import web
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage

import aioredis
from db import on_startup, on_shutdown

from aiohttp_security import SessionIdentityPolicy
from aiohttp_security import setup as setup_security
from db_auth import DBAuthorizationPolicy
from handlers import Web


async def init(loop: asyncio.AbstractEventLoop) -> Tuple[asyncio.Server, web.Application,
                                                         web.Server]:
    redis = aioredis.from_url("redis://localhost:6379")
    print(type(redis))
    print("AAA")
    print(aioredis.Redis)
    print("BBB")
    await on_startup()
    app = web.Application()
    setup_session(app, RedisStorage(redis))
    setup_security(app,
                   SessionIdentityPolicy(),
                   DBAuthorizationPolicy())

    web_handlers = Web()
    web_handlers.configure(app)

    handler = app.make_handler()
    srv = await loop.create_server(handler, '127.0.0.1', 8080)
    print('Server started at http://127.0.0.1:8080')
    return srv, app, handler


async def finalize(srv: asyncio.Server, app: web.Application, handler: web.Server) -> None:
    sock = srv.sockets[0]
    app.loop.remove_reader(sock.fileno())
    sock.close()

    await handler.shutdown(1.0)
    srv.close()
    await srv.wait_closed()
    await app.cleanup()

    await on_shutdown()


def main() -> None:
    loop = asyncio.get_event_loop()
    srv, app, handler = loop.run_until_complete(init(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete((finalize(srv, app, handler)))


if __name__ == '__main__':
    main()
