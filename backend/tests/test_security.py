from jwt import decode

from src.security import JWT
from src.settings import settings


def test_encode_jwt():
    data = {'test': 'test'}

    encoded = JWT.encode(data)

    decoded = decode(
        encoded, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded['test'] == data['test']
    assert decoded['exp']
