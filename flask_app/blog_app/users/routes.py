from flask import  render_template,url_for , flash ,redirect , request ,Blueprint
from   blog_app.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                               RequestResetForm,ResetPasswordForm)
from  blog_app.models import User, Post
from blog_app import db , bcrypt 
from flask_login import login_user, current_user, logout_user, login_required

from blog_app.users.utils import save_picture, send_reset_link

#----------------------------------------------------------------------------------------------
#creating the blueprint for user's package 

# from flask import Blueprint
users = Blueprint('users',__name__) #making the instance for the  'users' blueprint 

#-----------------------------------------------------------------------------------------------------
@users.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        user=User(username=form.username.data, email= form.email.data, password= hashed_password) #stroing hashed password
        db.session.add(user)
        db.session.commit()
        # flash(f'Account createed  for {form.username.data}!','success') #flask message flash , and bootstrap class  "success"
        flash(f'Account createed  for {form.username.data}! now you can login ','success')
        return redirect(url_for('users.login'))            
    return render_template('register.html',title='Register',form=form)
#-------------------------------------------------------------------------------------------------

@users.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=LoginForm()
    if form.validate_on_submit():
        #if form.email.data =='myblog@email.com' and form.password.data =='mypassword':
        user= User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data): #form.password.data to access the password string entered by the user:
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next') #if exists the next parameter in page route 
            return  redirect(next_page) if next_page else redirect(url_for('main.home')) #ternary condition
        else:
            flash('Login Failed , Try again with right Password and username','danger')
    return render_template('login.html',title='Login',form=form)
#--------------------------------------------------------------------------------------------

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

#-----------------------------------------------------------------------------

#route for the account section

@users.route('/account',methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))   #when you relode the page your browser is requesting another Post method
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    

    image_file= url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', 
                           image_file=image_file, form=form) #breaking line in pep 8 compline 

#------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# route  for the user posts 


@users.route('/user/<string:username>') #  creating the var. for userpost route as string
def user_posts(username):
    page= request.args.get('page',1,type=int) #for the different page route 
    user= User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
            .paginate(page=page,per_page=5) #pagination  defualt on page 5, and quering post on desc. order 
    return render_template('user_post.html',posts = posts, user=user)  # paasing the post and user to the user_post.html template

#----------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------
# route for the request reset password
#-----------------------------------------------------------------------------------

@users.route('/reset_password', methods =['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:  #this is check if user is logged out to access the reset route 
        return redirect(url_for('main.home'))
    form = RequestResetForm()   #from is submited then after validation

    if form.validate_on_submit():
        user= User.query.filter_by(email= form.email.data).first()
        send_reset_link(user)
        flash('An Email has been sent with instruction to reset your passwrd','info')
        return redirect(url_for('users.login'))
    
    return render_template('reset_request.html',title='Reset Password', form= form)

#---------------------------------------------------------------------------------------------------------

@users.route('/reset_password/<token>', methods =['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    user =User.verify_reset_token(token) 
    if user is None:
        flash('That is inavalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form= ResetPasswordForm()  #creating an instance of the ResetPasswordForm ,The parentheses are necessary to create a new instance of the class.
   
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        user.password =  hashed_password
        db.session.commit()
        flash(f'your password has been updated ,now you can login ','success')
        return redirect(url_for('users.login'))            
    return render_template('reset_token.html',title='Reset Password', form =form)
