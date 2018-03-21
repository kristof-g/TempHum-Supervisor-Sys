from server.helpers import resource_path
SECRET_KEY = "DEVELOPMENT-KEY-CHANGE-ASAP"
SQLALCHEMY_DATABASE_URI = "sqlite://"+resource_path("/database/database.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
#=========================================================
#           JavaScript Web Token
#=========================================================
JWT_SECRET_KEY = "JWT-SECRET"
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']