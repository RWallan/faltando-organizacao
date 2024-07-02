"""Cria a engine e expõe a session do db."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.settings import settings

engine = create_engine(settings.DATABASE)


def init_session():
    with Session(engine) as session:
        yield session
