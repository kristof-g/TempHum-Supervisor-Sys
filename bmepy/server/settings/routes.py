import sys
import json

from flask import Blueprint, render_template, session, redirect, request, url_for, jsonify

from server import db, ma
from server.settings.model import config, Station, StationSchema
from server.helpers import pwIsValid, LoginRequired

app = sys.modules['__main__']

show_cfg_page = Blueprint('show_cfg_page', __name__, template_folder='templates')
show_stations_page = Blueprint('show_stations_page', __name__, template_folder='templates')

@show_cfg_page.route('/show_cfg', methods=['GET', 'POST'])
def show_cfg():
    cfg = config.query.filter_by(id=1).first()
    return str(cfg.ip) +":"+ str(cfg.port)


@show_stations_page.route('/show_stations', methods=['GET', 'POST'])
def show_stations():
    stations = Station.query.all()
    stations_schema = StationSchema(many=True)
    output = stations_schema.dump(stations).data
    return jsonify({"allomasok" : output})