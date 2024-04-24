
import os 
import secrets #for random image name 
from PIL import Image
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
@app.route('/H+ome') # adding the multiple route within one fun using the  decorator
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

#--------------------------------------------------------------------
#func for the updating the new profile pic 

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #8 bytes string 
    _,f_text = os.path.splitext(form_picture.filename) #data and filename extension #_ for f_name
    picture_fn = random_hex + f_text
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    #for converting picture in small file
    ouput_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(ouput_size)
    i.save(picture_path)
   # form_picture.save(picture_path)

    return picture_fn
#----------------------------------------------------------------------------------

#route for the account section

@app.route('/account',methods=['GET', 'POST'])
@login_required # decorator for login required to access the content of web..
def account():
    form= UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file         
        current_user.username=form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))   #when you relode the page your browser is requesting another Post method
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    

    image_file= url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', 
                           image_file=image_file, form=form) #breaking line in pep 8 compline 

