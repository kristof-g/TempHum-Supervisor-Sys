from flask_restful import Resource
from server.user.model import UserModel


class AllStations(Resource):
    def get(self):
        return UserModel.return_all()
