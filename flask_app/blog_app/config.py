
#pUtting the all the configuration values here 
import os 

class Config:
    
    SECRET_KEY = '571feb486e78c8e055ade270a8e5fc'  #os.environ.get('SECRET_key') #Set it ias a environ var
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  #os.environ.get('SQLALCHEMY_DATABASE_URI')
    #/// are the relative path from the current file so site.db will be created

    #-------------------------------------------------------
    #Configration for email sending 
    #-----------------------------------------------------
    MAIL_SERVER= 'smtp.office365.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_USERNAME =   os.environ.get('MAIL_USER')
    MAIL_PASSWORD =   os.environ.get('MAIL_PASS')


#Note :  removed app.config['MAIL_USERNAME']  because we want only constant var. same name as key 

 