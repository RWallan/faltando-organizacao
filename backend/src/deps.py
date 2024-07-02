"""Dependências do projeto."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.database import init_session

Session = Annotated[Session, Depends(init_session)]
