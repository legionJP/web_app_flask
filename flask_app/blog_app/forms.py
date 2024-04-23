from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import DataRequired , Length, Email, EqualTo , ValidationError
from blog_app.models import User
class RegistrationForm(FlaskForm):
    username= StringField('Username',validators=[ DataRequired(),Length(min=2,max=20)])

    email= StringField('Email', validators=[ DataRequired(),Email()])

    password = PasswordField('Password', 
                             validators=[DataRequired(),Length(min=5)])
    confirm_password =PasswordField('Confirm Password', 
                                    validators= [DataRequired(), EqualTo('password')])

    submit =SubmitField('Sign up')

#creating the template for validation 

    def validate_field(self,username):
        user = User.query.filter_by(username=username.data).first()
        if User:
            raise ValidationError('This username is taken , please choose another one')
        
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if User:
            raise ValidationError('The email is already in use, please choose another one')
        

class LoginForm(FlaskForm):
    # username= StringField('Username',validators=[data_required(),Length(min=2,max=20)])
    email= StringField('Email', validators=[DataRequired(),Email()])

    password = PasswordField('Password', validators=[DataRequired(),Length(min=5)])
    remember = BooleanField('Remeber me')

    submit =SubmitField('Login')
 
#  #Note : when using these forms we needs the secret key for our app. , Secret key will protect against the modifying 
#  cookies and cross site request forgery attacks

# #generate secret key by py : 
# import secrets
# secrets.token_hex(16) #16bytes code

