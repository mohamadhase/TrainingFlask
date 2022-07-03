from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField
from wtforms.validators import DataRequired , Email , Length, EqualTo,ValidationError

from market.models import User
class RegisterForm(FlaskForm):

    username = StringField('User Name : ', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email : ', validators=[DataRequired(), Email()])
    password = PasswordField('Password : ', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password : ', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')


    
class LoginForm(FlaskForm):
    username = StringField('UserName : ', validators=[DataRequired()])
    password = PasswordField('Password : ', validators=[DataRequired()])
    submit = SubmitField('Submit')




class   PurchaseItemForm(FlaskForm):
    submit = SubmitField('Purchase Item!')

class SellItemForm(FlaskForm):
    submit = SubmitField('Sell Item!')


