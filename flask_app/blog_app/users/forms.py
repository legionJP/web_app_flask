from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField,BooleanField, TextAreaField
from wtforms.validators import DataRequired , Length, Email, EqualTo , ValidationError
from blog_app.models import User

#---------------------------------------------------------------------------------
class RegistrationForm(FlaskForm):
    username= StringField('Username',validators=[ DataRequired(),Length(min=2,max=20)])

    email= StringField('Email', validators=[ DataRequired(),Email()])

    password = PasswordField('Password', 
                             validators=[DataRequired(),Length(min=5)])
    confirm_password =PasswordField('Confirm Password', 
                                    validators= [DataRequired(), EqualTo('password')])

    submit =SubmitField('Sign up')

#creating the template for registration validation 

    def validate_username(self,username):
        user = User.query.filter_by( username=username.data).first()
        if user:
            raise ValidationError('This username is taken , please choose another one')
        
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email is already in use, please choose another one')
        

class LoginForm(FlaskForm):
    # username= StringField('Username',validators=[data_required(),Length(min=2,max=20)])
    email= StringField('Email', validators=[DataRequired(),Email()])

    password = PasswordField('Password', validators=[DataRequired(),Length(min=5)])
    remember = BooleanField('Remeber me')

    submit =SubmitField('Login')
 
#--------------------------------------------------------------------------- 
#  #Note : when using these forms we needs the secret key for our app. , Secret key will protect against the modifying 
#  cookies and cross site request forgery attacks
# #generate secret key by py : 
# import secrets
# secrets.token_hex(16) #16bytes code
#-----------------------------------------------------------------------------------

#------------------------------------
#Forms for the Updating the account :
#------------------------------------

class UpdateAccountForm(FlaskForm):
    username= StringField('Username',validators=[ DataRequired(),Length(min=2,max=20)])

    email= StringField('Email', validators=[ DataRequired(),Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])

    submit =SubmitField('Update')

    #creating the template for validation 

    def validate_username(self,username):
       # user = User.query.filter_by(username.data.first()
        if username.data != current_user.username:    # not validate when current username is equal to  update username 
            user = User.query.get(username.data)
            if user:
                raise ValidationError('This username is taken , please choose another one')
        
    def validate_email(self,email):
        if email.data != current_user.email:                
            user = User.query.get(email.data)
            if user:
                raise ValidationError('The email is already in use, please choose another one')
            
#----------------------------------------------------------------------------------------

#form for the password reset 

class RequestResetForm(FlaskForm):
        email= StringField('Email', validators=[ DataRequired(),Email()])
        submit = SubmitField('Request Password Reset!')

        def validate_email(self,email):
            user = User.query.filter_by(email=email.data).first()
            if user is None:
                raise ValidationError('No Account exists with this email, You need to create one!')
            
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', 
                             validators=[DataRequired(),Length(min=5)])
    confirm_password =PasswordField('Confirm Password', 
                                    validators= [DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Reset Password!')



            