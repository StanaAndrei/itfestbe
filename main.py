from flask import Flask, jsonify, make_response
from models import init_db
from controllers import initControllers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://app:password@192.168.56.101:3306/itfest"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False


if __name__ == '__main__':
    init_db(app)
    initControllers(app)
    app.run(port=5000)
