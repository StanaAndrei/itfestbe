from flask import request, make_response
from http import HTTPStatus
import jwt
from functools import wraps


def authMW(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        authHeader = request.headers.get('Authorization')
        if not authHeader:
            return make_response({}, HTTPStatus.UNAUTHORIZED)
        token = authHeader.split(' ')[1]
        print(authHeader)
        data = jwt.decode(token, 'secret', algorithms=['HS256'])
        try:
            userId = int(data.get('id'))
            return func(userId, *args, **kwargs)
        except Exception as e:
            print(e)
            return make_response({}, HTTPStatus.UNAUTHORIZED)

    return wrapper
