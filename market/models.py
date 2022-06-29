from email.policy import default
from market import db

class User(db.Model):
  id=db.Column(db.Integer, primary_key=True)
  username=db.Column(db.String(80), unique=True, nullable=False)
  email=db.Column(db.String(120), unique=True, nullable=False)
  password=db.Column(db.String(60), nullable=False)
  budget= db.Column(db.Integer, nullable=False,default=1000)
  items=db.relationship('Item', backref='user', lazy=True)
  def __repr__(self):
    return '<User %r>' % self.username


class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30),nullable=False,unique=True)
  price = db.Column(db.Integer(),nullable=False)
  barcode = db.Column(db.String(12),nullable=False,unique=True)
  description = db.Column(db.String(1024),nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  def __repr__(self) -> str:
     return f'Item {self.name}'
     
