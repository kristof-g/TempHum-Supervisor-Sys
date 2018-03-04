import json
import sys
import os
from helpers import logger
app = sys.modules['__main__']

def save_allomas():
    with open('allomasok.json', 'w') as fp:
            json.dump(app.GLOBAL_STATION_CONFIG, fp, sort_keys=True, indent=4)
    logger("ALLOMAS - CONFIG", "Saved...")


def save_cfg():
    try:
        with open('config.json', 'w') as fp:
                json.dump(app.GLOBAL_CONFIG, fp, sort_keys=True, indent=4)
    except Exception as error:
        logger("ALTALANOS - CONFIG", error)
    logger("ALTALANOS - CONFIG", "Changes saved...")
    logger("ALTALANOS - CONFIG", app.GLOBAL_CONFIG)


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def load_configs():
    path = resource_path("config.json")
    app.GLOBAL_CONFIG = json.load(open(path, encoding="utf-8"))
    path = resource_path("allomasok.json")
    app.GLOBAL_STATION_CONFIG = json.load(open(path, encoding="utf-8"))
    logger("CONFIGS","Loaded..")
