"""Router responsável pelas operações de usuários."""

from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src import deps, schemas
from src.database import models

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/', response_model=schemas.User, status_code=HTTPStatus.CREATED
)
def create_user(user: schemas.UserCreate, db: deps.Session) -> models.User:
    db_user = db.scalar(
        select(models.User).where(models.User.email == user.email)
    )

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Email já existe.'
        )

    db_user = models.User(**user.model_dump())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
