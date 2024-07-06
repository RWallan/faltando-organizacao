import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from src.app import app
from src.database import init_session, models, reg
from src.security import Hasher


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[init_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    reg.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    reg.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    user = models.User(
        name='Teste',
        email='test@test.com',
        password=Hasher.hash_password('test1234'),
        course='Teste',
    )

    user.clean_pwd = 'test1234'  # pyright: ignore

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
