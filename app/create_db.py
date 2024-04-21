from flask import app 
from app import db , Post
with app.app_context():
    # db.create_all()
    # user1= User(username='JPs',email= 'jppal12@gmail.com', password='password')
    # db.session.add(user1)
    # user2 =User(username='Swamis', email='snand12@gmail.com',password='password')
    # db.session.add(user2)
    # db.session.commit()
    post_1=Post(title='Blog_1',content ='First post of the blog', user_id= 1)
    db.session.add(post_1)
    post_2=Post(title='Blog_2',content ='Second post of the blog', user_id= 2)    
    db.session.add(post_2)
    db.session.commit()
    

