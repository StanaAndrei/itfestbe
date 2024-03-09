from flask import Blueprint, Flask, jsonify, make_response, request
from models.product import Product
from http import HTTPStatus
from middlewares.auth import authMW
from ai.ai import callAI

productBP = Blueprint('product-controller', __name__, url_prefix='/product')


@productBP.route('/', methods=['POST'])
@authMW
def addProduct(userId):
    json_data = request.get_json()

    name_value = json_data.get('name')
    description_value = json_data.get('description')
    image_value = json_data.get('image')
    energy_100g_value = json_data.get('energy_100g')
    proteins_100g_value = json_data.get('proteins_100g')
    carbohydrates_100g_value = json_data.get('carbohydrates_100g')
    sugars_100g_value = json_data.get('sugars_100g')
    fat_100g_value = json_data.get('fat_100g')
    saturated_fat_100g_value = json_data.get('saturated_fat_100g')
    fiber_100g_value = json_data.get('fiber_100g')
    salt_100g_value = json_data.get('salt_100g')
    category = json_data.get('category')
    health_score = callAI([
        energy_100g_value, proteins_100g_value, carbohydrates_100g_value, sugars_100g_value, fat_100g_value,
        saturated_fat_100g_value, fiber_100g_value, salt_100g_value
    ])

    try:
        Product.create(
            user_id=userId,
            name=name_value,
            description=description_value,
            image=image_value,
            energy_100g=energy_100g_value,
            proteins_100g=proteins_100g_value,
            carbohydrates_100g=carbohydrates_100g_value,
            sugars_100g=sugars_100g_value,
            fat_100g=fat_100g_value,
            saturated_fat_100g=saturated_fat_100g_value,
            fiber_100g=fiber_100g_value,
            salt_100g=salt_100g_value,
            category=category,
            health_score=health_score
        )
        return make_response({}, HTTPStatus.CREATED)
    except Exception as e:
        print(e)
        return make_response({}, HTTPStatus.INTERNAL_SERVER_ERROR)


@productBP.route('/')
def getProducts():
    try:
        products = Product.query.all()
        ans = []
        for product in products:
            ans.append(product.as_dict())
        return make_response({"products": ans}, HTTPStatus.OK)
    except Exception as e:
        return make_response({}, HTTPStatus.INTERNAL_SERVER_ERROR)


@productBP.route('/<name>')
def getProduct(name):
    try:
        product = Product.query.filter_by(name=name).first()
        return make_response(product.as_dict(), HTTPStatus.OK)
    except Exception as e:
        return make_response({}, HTTPStatus.INTERNAL_SERVER_ERROR)
