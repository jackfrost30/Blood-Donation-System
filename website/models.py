from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))

class Donate(db.Model):
    id1 = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    blood_group = db.Column(db.String(10))
    quantity = db.Column(db.String(150))
    district = db.Column(db.String(50))
    mob_no = db.Column(db.String(15))