from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer, JwtAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session

from config import JWT_SECRET_KEY
from db.database import get_db
from models import Admin
from .schema import AuthSchema, AuthResponseSchema
from .utils import verify_password, get_password_hash

admin_auth_router = APIRouter(prefix='/auth')

access_security = JwtAccessBearer(secret_key=JWT_SECRET_KEY, auto_error=True)
refresh_security = JwtRefreshBearer(secret_key=JWT_SECRET_KEY, auto_error=True)


@admin_auth_router.post('', response_model=AuthResponseSchema, tags=['Auth'])
async def auth(data: AuthSchema, session: Session = Depends(get_db)):
    user: Admin = session.scalar(select(Admin).where(Admin.login == data.login))

    if not user:
        raise HTTPException(status_code=401, detail="Bad username or password")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token = access_security.create_access_token(subject={'id': user.id},
                                                       expires_delta=timedelta(days=1))
    refresh_token = access_security.create_refresh_token(subject={'id': user.id},
                                                         expires_delta=timedelta(days=7))

    return {'access_token': access_token, 'refresh_token': refresh_token}


@admin_auth_router.post('/refresh', response_model=AuthResponseSchema, tags=['Auth'])
async def refresh(credentials: JwtAuthorizationCredentials = Security(refresh_security)):
    access_token = access_security.create_access_token(subject=credentials.subject,
                                                       expires_delta=timedelta(days=1))
    refresh_token = access_security.create_refresh_token(subject=credentials.subject,
                                                         expires_delta=timedelta(days=7))

    return {'access_token': access_token, 'refresh_token': refresh_token}


@admin_auth_router.post('/sign_in', tags=['Auth'])
async def sign_in(data: AuthSchema, session: Session = Depends(get_db)):
    # If Admin objects already exist - throw 404 to hide method
    if session.scalars(select(Admin)):
        return HTTPException(status_code=404)

    new_admin = Admin()
    new_admin.login = data.login
    new_admin.hashed_password = get_password_hash(data.password)

    session.add(new_admin)
    session.commit()
    return {'message': 'User created'}
