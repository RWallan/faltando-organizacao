from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from src import deps, schemas, security
from src.database import models

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=schemas.Token)
def login(db: deps.Session, form: OAuth2PasswordRequestForm = Depends()):
    user = db.scalar(
        select(models.User).where(models.User.email == form.username)
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado.'
        )

    if not security.Hasher.verify_password(form.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email ou senha incorreta.',
        )

    access_token = security.JWT.encode(data={'sub': user.id})

    return schemas.Token(access_token=access_token, token_type='bearer')
