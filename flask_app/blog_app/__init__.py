# app= Flask(__name__) #creatimg app variable Flask  and setiing it as a instance of class Flask 

#__name__ module will be equal to __main__ if be run the our py app directly 
#creating the route , by using app decorator 
# @app.route("/") #forward / is route page of our web

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



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

 
# from routes import routes
# from   blog_app import routes
from  blog_app import routes