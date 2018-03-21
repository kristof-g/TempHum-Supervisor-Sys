from flask_restful import Resource
from server.device.models import StationModel


class AllStations(Resource):
    def get(self):
        return StationModel.return_all()

    def delete(self):
        return StationModel.delete_all()
