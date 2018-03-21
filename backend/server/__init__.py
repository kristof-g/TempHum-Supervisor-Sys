# -*- coding: utf-8 -*-
# Web MicroFramework parts
from flask import Flask, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_jwt_extended import JWTManager

from server.helpers import LoginRequired, resource_path
from server.configuration import load_configs

app = Flask(__name__)
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)
from server.user.model import *
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
#   USER RES
#-------------------------------------------
from server.user import resources
api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')
