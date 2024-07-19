from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from fast_zero.database import get_session
from fast_zero.models import User

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRETE_KEY = 'secrete-key'  # TEMPORARIO
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data_claims: dict):
    to_encode = data_claims.copy()

    # ADICIONAR UM TEMPO DE EXPIRAÇÃO (30 min)
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    encode_jwt = encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)
    return encode_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credential_exception = HTTPException(
        HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Autenticate': 'Bearer'},
    )
    try:
        payload = decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')

        if not username:
            raise credential_exception
    except PyJWTError:
        raise credential_exception

    user = session.scalar(select(User).where(User.email == username))

    if not user:
        raise credential_exception

    return user
