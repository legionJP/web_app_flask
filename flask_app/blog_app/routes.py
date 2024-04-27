
import os 
import secrets #for random image name 
from PIL import Image
from flask import  render_template,url_for , flash ,redirect , request,abort

from   blog_app.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                              PostForm,RequestResetForm,ResetPasswordForm)

from  blog_app.models import User, Post
from blog_app import app, db , bcrypt ,mail
from flask_mail import Message
from flask_login import login_user, current_user, logout_user, login_required


# #making the list of dict for the post data
# posts = [
#     {
#         'author':'AK',
#         'title':'Blog post 2',
#         'content':'content of ak  Post will appear here',
#         'date_posted':'April 15 , 2024'        
#     },
#     { 
#         'author':'JP',
#         'title':'Blog post 1',
#         'content':'First Post Content',
#         'date_posted':'April 15 , 2024'
#     }
#]

#-------------------------------------------------------------------------------------------------------------------------
@app.route('/')
@app.route('/home') # adding the multiple route within one fun using the  decorator
def home():
    # posts=Post.query.all()
    page= request.args.get('page',1,type=int) #for the different page route 
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5) #pagination  defualt on page 5, and quering post on desc. order 
    return render_template('home.html',posts = posts) #passing the var to template so the data of posts will be equal to post data

#------------------------------------------------------------------------------------------
@app.route('/about')
def about():
    #return '<h1>Hello, this is flask app!</h1>'
    return render_template('about.html',title='About')

#-----------------------------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------------------------

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
#--------------------------------------------------------------------------------------------

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
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
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

#------------------------------------------------------------------------------


@app.route('/post/new', methods =['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        #adding the post on the database
        post= Post(title=form.title.data, content = form.content.data, author= current_user)
        db.session.add(post)
        db.session.commit()        
        flash('Your post has been created !', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form,legend= 'New Post')

#----------------------------------------------------------------------------------------------------------

#creating the routes where post_id is the part of the route 

@app.route('/post/<int:post_id>')  #Flask gives the ability to add variable within the routes 
def post(post_id):
    # post= Post.query.get(post_id)
    post= Post.query.get_or_404(post_id)
    return render_template('post.html', title = post.title, post =post) #passing the post var. to post template 

#-------------------------------------------------------------------------------------------------
@app.route('/post/<int:post_id>/update',  methods =['GET', 'POST']) 
@login_required  
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)    #403 is the HTTP response for forbidden route 
    form = PostForm()
    if form.validate_on_submit():
        post.title= form.title.data
        post.content= form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('post', post_id= post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content # this will fill up the data in update post 
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

#-------------------------------------------------------------------------------------------------------------
@app.route('/post/<int:post_id>/delete',  methods =[ 'POST']) 
@login_required  
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)    #403 is the HTTP response for forbidden route 
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted !', 'success')    
    return redirect(url_for('home'))


#--------------------------------------------------------------------------------
# route  for the user posts 


@app.route('/user/<string:username>') #  creating the var. for userpost route as string
def user_posts(username):
    page= request.args.get('page',1,type=int) #for the different page route 
    user= User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
            .paginate(page=page,per_page=5) #pagination  defualt on page 5, and quering post on desc. order 
    return render_template('user_post.html',posts = posts, user=user)  # paasing the post and user to the user_post.html template

#-----------------------------------------------------------------------------------------------------
# route for the request reset password
#-----------------------------------------------------------------------------------
def send_reset_link(user):
    token = user.get_reset_token()
    msg= Message('Password Reset Request',sender='bharat_tech@outlook.com', recipients=[user.email]) #for subject
    msg.body= f'''To reset your Password visit the following link:
{url_for('reset_token',token= token,_external=True)} the link is valid for 30 Minutes. If not requested by you , simpy ignore this email '''
    
    mail.send(msg)
    return 'sent'



@app.route('/reset_password', methods =['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:  #this is check if user is logged out to access the reset route 
        return redirect(url_for('home'))
    form = RequestResetForm()   #from is submited then after validation

    if form.validate_on_submit():
        user= User.query.filter_by(email= form.email.data).first()
        send_reset_link(user)
        flash('An Email has been sent with instruction to reset your passwrd','info')
        return redirect(url_for('login'))
    
    return render_template('reset_request.html',title='Reset Password', form= form)

#-----------------------------------------------------------------------------------------

@app.route('/reset_password/<token>', methods =['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    user =User.verify_reset_token(token)
    if user is None:
        flash('That is inavalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form= ResetPasswordForm

    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        user.password =  hashed_password
        db.session.commit()
        flash(f'your password has been updated for {form.username.data}! now you can login ','success')
        return redirect(url_for('login'))            
    return render_template('reset_token.html',title='Reset Password', form =form)

    
