from datetime import datetime, timedelta
from typing import Any

from jwt import encode
from zoneinfo import ZoneInfo

from src.settings import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


class JWT:
    @staticmethod
    def encode(data: dict[str, Any]) -> str:
        to_encode = data.copy()

        expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode.update({'exp': expire})
        encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt
