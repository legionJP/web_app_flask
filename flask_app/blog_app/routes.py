
from flask import  render_template,url_for , flash ,redirect , request
from   blog_app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from  blog_app.models import User, Post
from blog_app import app, db , bcrypt
from flask_login import login_user, current_user, logout_user, login_required


#making the list of dict for the post data
posts = [
    {
        'author':'AK',
        'title':'Blog post 2',
        'content':'content of ak  Post will appear here',
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        user=User(username=form.username.data, email= form.email.data, password= hashed_password) #stroing hashed password
        db.session.add(user)
        db.session.commit()
        # flash(f'Account createed  for {form.username.data}!','success') #flask message flash , and bootstrap class  "success"
        flash(f'Account createed  for {form.username.data}! now you can login ','success')
        return redirect(url_for('login')) 
           
    return render_template('register.html',title='Register',form=form)


@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        #if form.email.data =='myblog@email.com' and form.password.data =='mypassword':
        user= User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data): #form.password.data to access the password string entered by the user:
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next') #if exists the next parameter in page route 
            return  redirect(next_page) if next_page else redirect(url_for('home')) #ternary condition
        else:
            flash('Login Failed , Try again with right Password and username','danger')
    return render_template('login.html',title='Login',form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required # decorator for login required to access the content of web..
def account():
    form= UpdateAccountForm()
    image_file= url_for('static', filename='profile_pics/profile.jpg') # + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)