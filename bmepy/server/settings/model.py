from server import db, ma
class config(db.Model):
    __tablename__ = 'config'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.Text, default="localhost")
    port = db.Column(db.Integer)

class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True)
    device_ip = db.Column(db.Text, default="not known")
    name = db.Column(db.Text, unique=True)
    mintemp = db.Column(db.Integer)
    maxtemp = db.Column(db.Integer)

class StationSchema(ma.ModelSchema):
    class Meta:
        model= Station