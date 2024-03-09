from flask import Blueprint, Flask, jsonify, make_response, request
from models.fav import Fav
from http import HTTPStatus
from middlewares.auth import authMW
from models import db
from models.product import Product
from sqlalchemy.orm import joinedload

favBP = Blueprint('fav-controller', __name__, url_prefix='/fav')


@favBP.route('/')
@authMW
def getFavsOfUser(userId):
    try:
        fav_products = (
            db.session.query(Fav, Product)
            .join(Product, Fav.prod_id == Product.id)
            .filter(Fav.user_id == userId)
            .options(joinedload(Fav.product))  # Use joinedload to eagerly load the Product data
            .all()
        )
        ans = []
        for fav_prod in fav_products:
            ans.append(fav_prod[1].as_dict())
        return make_response(ans, HTTPStatus.OK)
    except Exception as e:
        print(e)
        return make_response({}, HTTPStatus.INTERNAL_SERVER_ERROR)


@favBP.route('/', methods=['POST'])
@authMW
def addFav(userId):
    data = request.get_json()
    prodId = data.get('prodId')
    try:
        Fav.create(user_id=userId, prod_id=prodId)
        return make_response({}, HTTPStatus.CREATED)
    except Exception as e:
        print(e)
        return make_response({}, HTTPStatus.INTERNAL_SERVER_ERROR)


@favBP.route('/', methods=['DELETE'])
@authMW
def removeFav(userId):
    data = request.get_json()
    prodId = data.get('prodId')
    try:
        Fav.query.filter_by(user_id=userId, prod_id=prodId).delete()
        return make_response({}, HTTPStatus.OK)
    except Exception as e:
        print(e)
        return make_response({}, HTTPStatus.INTERNAL_SERVER_ERROR)
