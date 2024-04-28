# app= Flask(__name__) #creatimg app variable Flask  and setiing it as a instance of class Flask 

#__name__ module will be equal to __main__ if be run the our py app directly 
#creating the route , by using app decorator 
# @app.route("/") #forward / is route page of our web
from flask_mail import Mail
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from blog_app.config import Config #


app = Flask(__name__,template_folder='templates')
app.config.from_object(Config)  #paasiing the Config object as configuration 

#----------------------------------------------------------------
#setting up the instance , and app is argument
#-----------------------------------------------------------
db=SQLAlchemy(app) #instance for sql db
bcrypt = Bcrypt(app) #for password hashing 
login_manager = LoginManager(app)
login_manager.login_view = 'users.login' #setting the login route for login view to manage login required , and for blueprint case putting the users blueprint first
login_manager.login_message_category ='info' #login message if access account without login 


mail = Mail(app)  #initializing the extension for Mail

#-----------------------------------------------------------------
# from routes import routes
# Importing the routes in Blueprint model , we have to import those blueprints objects from each of 
#the packages and register them with our routes 

from blog_app.users.routes import users  #importing the blueprint instance of users route
app.register_blueprint(users)

from blog_app.posts.routes import posts
app.register_blueprint(posts)

from blog_app.main.routes import main
app.register_blueprint(main)

# from  blog_app import routes


#APP config from object 