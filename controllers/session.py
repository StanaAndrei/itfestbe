from flask import Blueprint, Flask, jsonify, make_response, request
from models.user import User
from http import HTTPStatus
import jwt

sessionBP = Blueprint('session-controller', __name__, url_prefix='/session')


@sessionBP.route('/', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    try:
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            eId = jwt.encode({"id": str(user.id)}, 'secret', algorithm='HS256')
            return make_response({"token": str(eId)}, HTTPStatus.OK)
        else:
            return make_response({}, HTTPStatus.BAD_REQUEST)
    except Exception as e:
        print(e)
        return make_response({}, HTTPStatus.INTERNAL_SERVER_ERROR)
