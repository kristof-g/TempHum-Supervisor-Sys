# -*- coding: utf-8 -*-
# Web MicroFramework parts
from flask import Flask, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from server.helpers import LoginRequired, resource_path
from server.configuration import load_configs

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
ma = Marshmallow(app)
import server.database

# GLOBAL CONFIGURATIONS
GLOBAL_STATION_CONFIG = {}
GLOBAL_CONFIG = {}

#-------------------------------------------
#   loading Blueprints for routes
#-------------------------------------------
from server.settings.routes import settings_bp
from server.user.routes import user_bp
from server.device.routes import device_bp
app.register_blueprint(settings_bp, url_prefix='/settings')

app.register_blueprint(user_bp)

app.register_blueprint(device_bp)


@app.before_first_request
def startup():
    #cfg.load_configs()
    pass


@app.route('/')
@LoginRequired
def allomasok():
    load_configs()
    ctx = {
        "ipcim": "fakeip:7234",
        "data": GLOBAL_STATION_CONFIG
    }
    return render_template('start.html', ctx=ctx)


@app.route("/getcsv", methods=['GET'])
@LoginRequired
def get_plot_csv():
    if request.method == 'GET':
        file_nev = request.args.get('f')
        fajlPath = os.path.join(GLOBAL_CONFIG['SERVER']['WORKDIR'], "downloads/{}".format(file_nev))
        with open(fajlPath) as fp:
            fajl = fp.read()
        return Response(
            fajl,
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename="+file_nev})
