
# app= Flask(__name__) #creatimg app variable Flask  and setiing it as a instance of class Flask 

#__name__ module will be equal to __main__ if be run the our py app directly 
#creating the route , by using app decorator 
# @app.route("/") #forward / is route page of our web


from flask import Flask, render_template,url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__,template_folder='templates')

app.config['SECRET_KEY'] = '571feb486e78c8e055ade270a8e5fc'

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


@app.route('/register')
def register():
    form=RegistrationForm()
    return render_template('register.html',title='Register',form=form)


@app.route('/login')
def login():
    form=LoginForm()
    return render_template('login.html',title='Login',form=form)





if __name__ == '__main__':
    app.run(debug=True) # it is equal to set DEBUG = 1
