from server import db
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    usrname = db.Column(db.String(15), unique=True)
    pw = db.Column(db.String(50), unique=True)