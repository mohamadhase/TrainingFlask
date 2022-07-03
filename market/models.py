from email.policy import default
from market import db,bcrypt
from flask_login import UserMixin
class User(db.Model, UserMixin):
  id=db.Column(db.Integer, primary_key=True)
  username=db.Column(db.String(80), unique=True, nullable=False)
  email=db.Column(db.String(120), unique=True, nullable=False)
  password_hashed=db.Column(db.String(60), nullable=False)
  budget= db.Column(db.Integer, nullable=False,default=1000)
  items=db.relationship('Item', backref='user', lazy=True)
  def __repr__(self):
    return '<User %r>' % self.username
  @property
  def password(self):
    return self.password_hashed

  @password.setter
  def password(self, password):
    self.password_hashed = bcrypt.generate_password_hash(password).decode('utf-8')
  
  def check_password_correction(self, attempted_password):
    return bcrypt.check_password_hash(self.password_hashed, attempted_password)

  @property
  def priettier_budget(self):
    if len(str(self.budget))>=4:
      return str(self.budget)[:-3]+','+str(self.budget)[-3:]+' $'
   
    else:
      return str(self.budget) + ' $'

  def can_purchase(self, item_price):
    return self.budget >= item_price



class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30),nullable=False,unique=True)
  price = db.Column(db.Integer(),nullable=False)
  barcode = db.Column(db.String(12),nullable=False,unique=True)
  description = db.Column(db.String(1024),nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  def __repr__(self) -> str:
     return f'Item {self.name}'

  def buy(self, user):
    if user.can_purchase(self.price):
      self.user_id = user.id
      user.budget -= self.price
      db.session.commit()
      return True
    return False

  def sell(self, user):
    if self.user_id == user.id:
      self.user_id = None
      user.budget += self.price
      db.session.commit()
      return True
    return False
     
