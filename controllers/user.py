from flask import Blueprint, Flask, jsonify, make_response, request
from models.user import User
from http import HTTPStatus

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

