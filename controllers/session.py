from flask import Blueprint, Flask, jsonify, make_response, request
from models.user import User
from http import HTTPStatus
import jwt
from flask_cors import CORS, cross_origin


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

@sessionBP.route('/', methods=['OPTIONS'])
def myfun():
    response = make_response()

    # Add CORS headers to the response
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")

    return response, HTTPStatus.OK
