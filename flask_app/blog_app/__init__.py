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




db=SQLAlchemy() #instance for sql db
bcrypt = Bcrypt() #for password hashing 
login_manager = LoginManager()
login_manager.login_view = 'users.login' #setting the login route for login view to manage login required , and for blueprint case putting the users blueprint first
login_manager.login_message_category ='info' #login message if access account without login 

mail = Mail()  #initializing the extension for Mail

#Creation of app through a function , 
#where the app creation will be inside of it  and extensions outsides of the fuctions
# because we don't want extentions inside the function
# but still need to intialize the these extensions inside of the functions 

'''
because
,the extension object does not initially get bound to application, using this design pattern no app. secific state
is stroed on the extension object , so one extension object can be used for multiple apps.
so, Intializing the extensions at the top , without app variable
'''

def create_app(config_class=Config):
    
    app = Flask(__name__,template_folder='templates')
    app.config.from_object(Config)  #paasiing the Config object as configuration 

    db.init_app(app)        #running the .init_app() method and passing app var.
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    #importing the blueprint instance of users route
    from blog_app.users.routes import users  
    app.register_blueprint(users)
    from blog_app.posts.routes import posts
    app.register_blueprint(posts)
    from blog_app.main.routes import main
    app.register_blueprint(main)

    return app



'''
#----------------------------------------------------------
#setting up the instance , and app as a argument
#----------------------------------------------------------

app = Flask(__name__,template_folder='templates')
app.config.from_object(Config)  #paasiing the Config object as configuration 

db=SQLAlchemy(app) #instance for sql db
bcrypt = Bcrypt(app) #for password hashing 
login_manager = LoginManager(app)
login_manager.login_view = 'users.login' #setting the login route for login view to manage login required , and for blueprint case putting the users blueprint first
login_manager.login_message_category ='info' #login message if access account without login 

mail = Mail(app)  #initializing the extension for Mail
'''

#-----------------------------------------------------------------
 # from  blog_app import routes
#instead of this we have to - 
# Importing the routes in Blueprint model , we have to import those blueprints objects from each of 
#the packages and register them with our routes 

#-------------------------------------------------------------------------------

#APP config from object 



