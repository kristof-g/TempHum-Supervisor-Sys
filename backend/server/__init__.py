# -*- coding: utf-8 -*-
# Web MicroFramework parts
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_jwt_extended import JWTManager

from server.helpers import LoginRequired, resource_path
from server.configuration import load_configs

app = Flask(__name__, static_url_path='', static_folder='front')
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)
from server.user.model import *
from server.device.models import *
db.create_all()


ma = Marshmallow(app)
api = Api(app)
jwt = JWTManager(app)
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)

# GLOBAL CONFIGURATIONS
GLOBAL_STATION_CONFIG = {}
GLOBAL_CONFIG = {}

#-------------------------------------------
#   USER REST API
#-------------------------------------------
from server.user import resources as user_res
api.add_resource(user_res.UserRegistration, '/registration')
api.add_resource(user_res.UserLogin, '/login')
api.add_resource(user_res.UserLogoutAccess, '/logout/access')
api.add_resource(user_res.UserLogoutRefresh, '/logout/refresh')
api.add_resource(user_res.TokenRefresh, '/token/refresh')
api.add_resource(user_res.AllUsers, '/users')
api.add_resource(user_res.SecretResource, '/secret')

#-------------------------------------------
#   DEVICE REST API
#-------------------------------------------
from server.device import resources as device_res
api.add_resource(device_res.AllStations, '/stations')

from server.front import client_bp
app.register_blueprint(client_bp)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response