from flask import  render_template,  request , Blueprint
from  blog_app.models import User, Post

#--------------------------------------------------------------------------------------------------------------
# from flask import Blueprint
main = Blueprint('main',__name__) #making the instance for the  'users' blueprint 

#-------------------------------------------------------------------------------------------------------------------------
@main.route('/')
@main.route('/home') # adding the multiple route within one fun using the  decorator
def home():
    # posts=Post.query.all()
    page= request.args.get('page',1,type=int) #for the different page route 
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5) #pagination  defualt on page 5, and quering post on desc. order 
    return render_template('home.html',posts = posts) #passing the var to template so the data of posts will be equal to post data

#------------------------------------------------------------------------------------------
@main.route('/about')
def about():
    #return '<h1>Hello, this is flask main!</h1>'
    return render_template('about.html',title='About')
#--------------------------------------------------------------------------------------------