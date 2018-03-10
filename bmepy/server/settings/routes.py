import sys

from flask import Blueprint, render_template, session, redirect, request, url_for, jsonify

from server.settings.model import config, Station, StationSchema
from server.helpers import pwIsValid, LoginRequired

app = sys.modules['__main__']

settings_bp = Blueprint('settings_bp', __name__, template_folder='templates')

@settings_bp.route('/show_cfg', methods=['GET', 'POST'])
def show_cfg():
    cfg = config.query.filter_by(id=1).first()
    return str(cfg.ip) +":"+ str(cfg.port)


@settings_bp.route('/show_stations', methods=['GET', 'POST'])
def show_stations():
    stations = Station.query.all()
    stations_schema = StationSchema(many=True)
    output = stations_schema.dump(stations).data
    return jsonify({"allomasok" : output})