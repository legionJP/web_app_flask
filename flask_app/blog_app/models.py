
#==================================================================================================#
# from app import db   
# to cop with the circular import use:
# from __main__ import db #for this import the USER and Model in app.py after the db var.

# db.init_app(app)
# with app.app_context():

#     # You can use Flask's functionality here
#  db.create_all()

#================================================================================================#
'''
In SQLAlchemy we can represents data structures as class called Models
'''
from blog_app import   db, login_manager 
from flask import current_app #removing 'app' and importing the current app which is inside of our flask package
import time
from datetime import datetime  
from sqlalchemy.sql import func
from flask_login import UserMixin 
from itsdangerous import URLSafeTimedSerializer,SignatureExpired , Serializer



@login_manager.user_loader # this is decorator for querying user_id , and The function you set should take a user ID
def load_user(user_id):
    return User.query.get(int(user_id))

#above extenstion will inspect the user model with four aspect 1. to be exact one(authenticate) returns true if match
#2. is active 3. is_anonymous 4. get_id method . The class method for all these is UserMixin


#creating model class for user model

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique = True , nullable= False)
    email = db.Column(db.String(100), unique = True , nullable= False)
    image_file =db.Column(db.String(20), nullable =False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts= db.relationship('Post', backref =  'author' , lazy = True)
    # 'Post' becaue it using Post module class
    #one to many relationship and this is not column but running the query in additional

#-------------------------------------------------------------------------------------------------------
    #creating function for the token generation for password reset
    def get_reset_token(self, expire_sec=1800):
        s= URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id':self.id, 'exp':time.time()+expire_sec})  #user_id is the payloads
    
    @staticmethod      #here telling to not accept the token as a self param  but accept as token argument 
    def verify_reset_token(token):
        s= URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id= s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)   # we will get the user by the user_id
    
    
    def __repr__(self):  #will return the data of the objects to how it is going to print
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable =False)
    date_posted = db.Column(db.DateTime, nullable = False , default = func.now())
    content = db. Column(db.Text ,nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable =False) #user_id is refe. to table name and column name 


    def __repr__(self) -> str:
        return f"Post('{self.title}', '{self.date_posted}')"

#==========================================================================================================#

#-------------------------------------------------------    
#Adding the data on site.db file in User and Post Model
#--------------------------------------------------------

#from sqlalchemy.exc import IntegrityError   
# with app.app_context():
#     db.create_all()
    # user1= User(username='user10',email= 'user10@gmail.com', password='password')
    # user2 =User(username='User12', email='user12@gmail.com',password='password')
    # db.session.add(user1)
    # db.session.add(user2)    
    # try:
    #  db.session.commit()
    # except IntegrityError:
    #  db.session.rollback()

    # post_1=Post(title='Blog_10',content ='First post of the blog', user_id= user1.id)
    # post_2=Post(title='Blog_12',content ='Second post of the blog', user_id= user2.id)
    # db.session.add(post_1)
    # db.session.add(post_2)
    # try:
    #  db.session.commit()
    # except IntegrityError:
    #  db.session.rollback()
    # # User.query.all()    
    # # Post.query.all()
    # # db.drop_all()
    

#=========================================================================================================#

