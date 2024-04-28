from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField,  TextAreaField
from wtforms.validators import DataRequired  
 
#--------------------------------------------------------------------
#form for the writing the post
class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    submit= SubmitField('Post') #title of the submit button

#------------------------------------------------------------------------------