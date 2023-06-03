from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt
from jwt import exceptions
class JwtQueryParamsAuthentication(BaseAuthentication):

    def authenticate(self, request):

        #获取token并判断token的合法性
        token = request.COOKIES.get('token')

        SALT = settings.SECRET_KEY
        try:
            payload = jwt.decode(token,SALT,algorithms=['HS256'])
        except exceptions.ExpiredSignatureError:
            print('失效')
            raise AuthenticationFailed({'code': 1003, 'error': 'token已失效'})
        except jwt.DecodeError:
            print('认证失败')

            raise AuthenticationFailed({'code': 1003, 'error': 'token认证失败'})
        except jwt.InvalidTokenError:
            print('非法的认证失败')

            raise AuthenticationFailed({'code': 1003, 'error': '非法的token失败'})
        #三种操作
        #1.跑出异常，后续不在执行
        #2.return 一个元祖（1,2），认证通过；在视图中如果调用request.user就是元组的第一个值，request.auth就是元组的第二个值
        #3.None
        return (payload,token)


