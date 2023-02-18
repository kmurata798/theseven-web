from app import app, db
from datetime import datetime, time

# Model - represents table in database
class SupportTicket(db.Model):
    __tablename__='tickets'
    # every model in SQLAlchemy needs primary key/unique id
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    # unique=true means email can only be inserted into table one time
    email = db.Column(db.String(100), unique=True)
    message = db.Column(db.String(300))
    # utcnow returns date time object, since im using date column, it will cut off time and use date
    # date_sent = db.Column(db.DateTime, default=datetime.utcnow)
    date_sent = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, name, email, message, date_sent=None):
        if date_sent is not None:
            self.date_sent=date_sent
        self.name=name
        self.email=email
        self.message=message

class Item(db.Model):
    __tablename__='items'
    # every model in SQLAlchemy needs primary key/unique id
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    # utcnow returns date time object, since im using date column, it will cut off time and use date
    date_released = db.Column(db.Date, default=datetime.utcnow)

    def __init__(self, name, price, date_released):
        self.name=name
        self.price=price
        self.date_released=date_released