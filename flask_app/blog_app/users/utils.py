
import os 
import secrets #for random image name 
from PIL import Image 
from blog_app import  mail 
from flask_mail import Message
from flask import  url_for,current_app 
#removing 'app' and importing the current app which is inside of our flask package.
#app import is no longer needed because it doesn't exits because we have put it inside of the create_app

 
#--------------------------------------------------------------------
#func for the updating the new profile pic 

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #8 bytes string 
    _,f_text = os.path.splitext(form_picture.filename) #data and filename extension #_ for f_name
    picture_fn = random_hex + f_text
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    #for converting picture in small file
    output_size = (200,200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
   # form_picture.save(picture_path)

    return picture_fn
#----------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------
#  send mail function to request reset password
#-----------------------------------------------------------------------------------
def send_reset_link(user):
    token = user.get_reset_token()
    msg= Message('Password Reset Request',sender='bharat_tech@outlook.com', recipients=[user.email]) #for subject
    msg.body= f'''To reset your Password visit the following link:
{url_for('users.reset_token',token= token,_external=True)} the link is valid for 30 Minutes. If not requested by you , simpy ignore this email '''
    
    mail.send(msg)
    return 'sent'


    