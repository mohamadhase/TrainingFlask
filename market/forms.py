from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField

class RegisterForm(FlaskForm):
    username = StringField('User Name : ')
    email = StringField('Email : ')
    password = PasswordField('Password : ')
    confirm_password = PasswordField('Confirm Password : ')
    submit = SubmitField('Submit')
    

    # def validate(self):
    #     if not super().validate():
    #         return False
    #     if self.password.data != self.confirm_password.data:
    #         self.confirm_password.errors.append('Passwords do not match')
    #         return False
    #     return True
