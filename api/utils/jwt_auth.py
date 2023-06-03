import jwt
import datetime
from django.conf import settings
def create_token(payload,timeout=7):
    SALT = settings.SECRET_KEY
    headers = {
        'typ': 'jwt',
        'alg': 'HS256',
    }
    # 构造payload
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=timeout)  # 超时时间
    token = jwt.encode(payload=payload, key=SALT, algorithm='HS256', headers=headers)

    return token