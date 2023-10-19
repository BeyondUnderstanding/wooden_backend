import os
import random
import string

import aiofiles
from fastapi import APIRouter, Depends, Security, UploadFile, File
from fastapi_jwt import JwtAuthorizationCredentials
from mypy_boto3_s3.client import S3Client
from sqlalchemy.orm import Session

from db.database import get_db
from modules.admin.auth.router import access_security
from utils import make_s3
from .schema import UploadResponseSchema

s3router = APIRouter(prefix='/objects', tags=['S3'])


@s3router.post('', response_model=UploadResponseSchema)
async def upload(
        file: UploadFile = File(),
        # CRINGE
        session: Session = Depends(get_db),
        auth: JwtAuthorizationCredentials = Security(access_security),
        s3: S3Client = Depends(make_s3)):
    filename = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=5)) + \
               file.filename

    async with aiofiles.open(filename, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
    s3.upload_file(filename, 'wooden', filename)
    os.remove(filename)
    return {'url': f'https://storage.yandexcloud.net/wooden/{filename}'}
