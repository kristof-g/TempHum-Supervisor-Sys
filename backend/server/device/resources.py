from flask_restful import Resource
from server.device.models import StationModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)


class AllStations(Resource):
    @jwt_required
    def get(self):
        return StationModel.return_all()

    def delete(self):
        return StationModel.delete_all()
