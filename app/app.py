from flask import Flask

app= Flask(__name__) #creatimg app variable Flask  and setiing it as a instance of class Flask 

#__name__ module will be equal to __main__ if be run the our py app directly 

#creating the route , by using app decorator 


# @app.route("/") #forward / is route page of our web

from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/Home') # adding the multiple route within one fun using the  decorator
def home():
    return '<h1>Home Page</h1>'

@app.route('/about')
def about():
    return '<h1>Hello, this is flask app!</h1>'





if __name__ == '__main__':
    app.run(debug=True) # it is equal to set DEBUG = 1
