
# app= Flask(__name__) #creatimg app variable Flask  and setiing it as a instance of class Flask 

#__name__ module will be equal to __main__ if be run the our py app directly 
#creating the route , by using app decorator 
# @app.route("/") #forward / is route page of our web


from flask import Flask, render_template,url_for , flash ,redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__,template_folder='templates')


app.config['SECRET_KEY'] = '571feb486e78c8e055ade270a8e5fc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#/// are the relative path from the current file so site.db will be created

db=SQLAlchemy(app) #setting up the instance , and app is argument
# db.init_app(app)
with app.app_context():

    # You can use Flask's functionality here
 db.create_all()
'''
In SQLAlchemy we can represents data structures as class called Models
'''
#creating model class for user model

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique = True , nullable= False)
    email = db.Column(db.String(100), unique = True , nullable= False)
    image_file =db.Column(db.String(20), nullable =False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts= db.relationship('Post', backref = 'author' , lazy = True)
    # 'Post' becaue it using Post module class
    #one to many relationship and this is not column but running the query in additional

    def __repr__(self) -> str: #will return the data of the objects to how it is going to print
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

import datetime  

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable =False)
    date_posted = db.Column(db.DateTime, nullable = False , default = datetime.UTC)
    content = db. Column(db.Text ,nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable =False) #user_id is refe. to table name and column name 


    def __repr__(self) -> str:
        return f"Post('{self.title}', '{self.date_posted}')"


#making the list of dict for the post data
posts = [
    {
        'author':'AK',
        'title':'Blog post 2',
        'content':'more Post Content',
        'date_posted':'April 15 , 2024'        
    },
    { 
        'author':'JP',
        'title':'Blog post 1',
        'content':'First Post Content',
        'date_posted':'April 15 , 2024'
    }
]


@app.route('/')
@app.route('/Home') # adding the multiple route within one fun using the  decorator
def home():
    #return '<h1>Home Page</h1>'
    return render_template('home.html',posts = posts) #passing the var to template so the data of posts will be equal to post data


@app.route('/about')
def about():
    #return '<h1>Hello, this is flask app!</h1>'
    return render_template('about.html',title='About')


@app.route('/register', methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account createed  for {form.username.data}!','success') #flask message flash , and bootstrap class  "success"
        return redirect(url_for('home'))    
    return render_template('register.html',title='Register',form=form)


@app.route('/login',methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data =='myblog@email.com' and form.password.data =='mypassword':
            flash('You are now loged in ','success')
            return redirect(url_for('home'))
        else:
            flash('Login Failed , Try again with right Password and username','danger')
    return render_template('login.html',title='Login',form=form)



if __name__ == '__main__':
    app.run(debug=True) # it is equal to set DEBUG = 1
