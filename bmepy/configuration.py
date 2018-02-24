import json, os
config = {}
allomasokconfig = None

def saveAllomas():
    with open('allomasok.json', 'w') as fp:
            json.dump(allomasokconfig, fp, sort_keys=True, indent=4)

def loadConfigs():
    global config, allomasokconfig
    dir = os.path.dirname(__file__)
    path = os.path.join(dir,"config.json")
    config = json.load(open(path, encoding="utf-8"))
    print(config)
    path = os.path.join(dir,"allomasok.json")
    allomasokconfig = json.load(open(path, encoding="utf-8"))
    print("|SERVER|: CONFIG LOADED")