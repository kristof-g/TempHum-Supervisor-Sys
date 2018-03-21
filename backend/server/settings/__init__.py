from server.settings.model import config
from server import db
db.create_all()
cfg = config.query.filter_by(id=1).first()
print(cfg.ip)