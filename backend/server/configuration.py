import json
import sys
from server.helpers import logger, resource_path
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
    load_configs()
    logger("ALTALANOS - CONFIG", app.GLOBAL_CONFIG)


def load_configs():
    path = resource_path("config.json")
    app.GLOBAL_CONFIG = json.load(open(path, encoding="utf-8"))
    path = resource_path("allomasok.json")
    app.GLOBAL_STATION_CONFIG = json.load(open(path, encoding="utf-8"))
    logger("CONFIGS","Loaded..")
    logger("CONFIGS", app.GLOBAL_CONFIG)

