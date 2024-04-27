# app= Flask(__name__) #creatimg app variable Flask  and setiing it as a instance of class Flask 

#__name__ module will be equal to __main__ if be run the our py app directly 
#creating the route , by using app decorator 
# @app.route("/") #forward / is route page of our web
from flask_mail import Mail
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# import os


app = Flask(__name__,template_folder='templates')

app.config['SECRET_KEY'] = '571feb486e78c8e055ade270a8e5fc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#/// are the relative path from the current file so site.db will be created

#----------------------------------------------------------------
#setting up the instance , and app is argument
#-----------------------------------------------------------
db=SQLAlchemy(app) #instance for sql db
bcrypt = Bcrypt(app) #for password hashing 
login_manager = LoginManager(app)
login_manager.login_view = 'login' #setting the login route for login view to manage login required 
login_manager.login_message_category ='info' #login message if access account without login 


#Configration for email sending 
app.config['MAIL_SERVER']= 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True 
app.config['MAIL_USE_SSL'] = False 
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASS')
app.config['MAIL_USERNAME'] =  'bharat_tech@outlook.com'
app.config['MAIL_PASSWORD'] =  'Worldoftechishere@23'





mail = Mail(app)  #initializing the extension for Mail


 
# from routes import routes
# from   blog_app import routes
from  blog_app import routes