from server.helpers import resource_path
SECRET_KEY = 'VBXXXVK7VzbBvWdx8lHqNy90FWb1a643'
SQLALCHEMY_DATABASE_URI = "sqlite://"+resource_path("/database/database.db")
DEBUG = True
PORT = 234