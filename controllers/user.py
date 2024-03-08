from flask import Blueprint, Flask, jsonify, make_response, request
from models.user import User
from http import HTTPStatus
from middlewares.auth import authMW


userBP = Blueprint('session-controller', __name__, url_prefix='/api/user')


@userBP.route("/", methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    try:
        User.create_user(username=username, email=email, password=password)
    except Exception as e:
        print(e)
        return make_response({}, HTTPStatus.INTERNAL_SERVER_ERROR)

    return make_response({}, HTTPStatus.CREATED)


@userBP.route('/')
@authMW
def getUser(userId):
    try:
        user = User.query.filter_by(id=userId).first()
    except Exception as e:
        print(e)
        return make_response({}, HTTPStatus.INTERNAL_SERVER_ERROR)
    return make_response(user.as_dict(), HTTPStatus.OK)
