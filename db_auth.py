from enum import Enum
from typing import Optional, Union

from passlib.hash import sha256_crypt

from aiohttp_security.abc import AbstractAuthorizationPolicy
from models import Users


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self):
        pass

    async def authorized_userid(self, identity: str) -> Optional[str]:
        user_exists = await Users.exists(login=identity, disabled=False)
        return identity if user_exists else None

    async def permits(self, identity: Optional[str], permission: Union[str, Enum],
                      context: None = None) -> bool:
        user = await Users.get_or_none(login=identity, disabled=False)
        if user is not None:
            if user.is_superuser:
                return True
            return permission in [perm.perm_name for perm in await user.permissions.all()]
        return False


async def check_credentials(username: str, password: str) -> bool:
    user = await Users.get_or_none(login=username, disabled=False)
    if user is not None:
        hashed = user.passwd
        return sha256_crypt.verify(password, hashed)
    return False
