"""Router responsável pelas operações de usuários."""

from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src import deps, schemas, security
from src.database import models

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=schemas.User, status_code=HTTPStatus.CREATED)
def create_user(user: schemas.UserCreate, db: deps.Session) -> models.User:
    db_user = db.scalar(
        select(models.User).where(models.User.email == user.email)
    )

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Email já existe.'
        )

    db_user = models.User(
        name=user.name,
        email=user.email,
        password=security.Hasher.hash_password(user.password),
        course=user.course,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get('/{id}', response_model=schemas.User)
def get_user_by_id(id: int, db: deps.Session) -> models.User:
    db_user = db.scalar(select(models.User).where(models.User.id == id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado.'
        )

    return db_user


@router.put(
    '/{id}', response_model=schemas.User, status_code=HTTPStatus.CREATED
)
def update_user(id: int, user: schemas.UserUpdate, db: deps.Session):
    db_user = db.scalar(select(models.User).where(models.User.id == id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado.'
        )

    user_in = user.model_dump(exclude_unset=True)
    if user_in.get('password'):
        user_in['password'] = security.Hasher.hash_password(
            user_in['password']
        )
    for field in user_in:
        setattr(db_user, field, user_in[field])

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.delete('/{id}', response_model=schemas.Message)
def delete_user(id: int, db: deps.Session):
    db_user = db.scalar(select(models.User).where(models.User.id == id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado.'
        )

    db.delete(db_user)
    db.commit()

    return schemas.Message(msg='Usuário deletado.')
