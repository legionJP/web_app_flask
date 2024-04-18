from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import DataRequired , Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username= StringField('Username',validators=[ DataRequired(),Length(min=2,max=20)])

    email= StringField('Email', validators=[ DataRequired(),Email()])

    password = PasswordField('Password', 
                             validators=[DataRequired(),Length(min=5)])
    confirm_password =PasswordField('Confirm Password', 
                                    validators= [DataRequired(), EqualTo('password')])

    submit =SubmitField('Sign up')
 
class LoginForm(FlaskForm):
    # username= StringField('Username',validators=[data_required(),Length(min=2,max=20)])
    email= StringField('Email', validators=[DataRequired(),Email()])

    password = PasswordField('Password', validators=[DataRequired(),Length(min=5)])
    remeber = BooleanField('Remeber me')

    submit =SubmitField('Login')
 
#  #Note : when using these forms we needs the secret key for our app. , Secret key will protect against the modifying 
#  cookies and cross site request forgery attacks

# #generate secret key by py : 
# import secrets
# secrets.token_hex(16) #16bytes code

