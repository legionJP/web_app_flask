from flask import Blueprint
from flask import  render_template,url_for , flash ,redirect , request,abort
from   blog_app.posts.forms import  PostForm 
from  blog_app.models import  Post
from blog_app import  db 
from flask_login import  current_user,   login_required

#-------------------------------------------------------------------
posts = Blueprint('posts',__name__) #making the instance for the  'users' blueprint 

#-----------------------------------------------------

@posts.route('/post/new', methods =['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        #adding the post on the database
        post= Post(title=form.title.data, content = form.content.data, author= current_user)
        db.session.add(post)
        db.session.commit()        
        flash('Your post has been created !', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form,legend= 'New Post')

#----------------------------------------------------------------------------------------------------------

#creating the routes where post_id is the part of the route 

@posts.route('/post/<int:post_id>')  #Flask gives the ability to add variable within the routes 
def post(post_id):
    # post= Post.query.get(post_id)
    post= Post.query.get_or_404(post_id)
    return render_template('post.html', title = post.title, post =post) #passing the post var. to post template 

#-------------------------------------------------------------------------------------------------
@posts.route('/post/<int:post_id>/update',  methods =['GET', 'POST']) 
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
        return redirect(url_for('posts.post', post_id= post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content # this will fill up the data in update post 
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

#-------------------------------------------------------------------------------------------------------------
@posts.route('/post/<int:post_id>/delete',  methods =[ 'POST']) 
@login_required  
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)    #403 is the HTTP response for forbidden route 
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted !', 'success')    
    return redirect(url_for('main.home'))

