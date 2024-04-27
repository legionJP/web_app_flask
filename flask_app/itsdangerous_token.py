
import os
# # Sign a user ID in a URL and email it to them to unsubscribe from a newsletter. 
# # This way you don’t need to generate one-time tokens and store them in the database.
# # Same thing with any kind of activation link for accounts and similar things.

from itsdangerous import URLSafeTimedSerializer,SignatureExpired
s= URLSafeTimedSerializer('secret',salt='verification')
token = s.dumps({'your_id':12},salt='verification') #generTE THE TOKEN 
try:
    data = s.loads(token,max_age=120) #decode the token if we want to verify it 
    print(token)
    print(data)   #gives the data payload
    token_utf8 = token.encode('utf-8')
    print(token_utf8)
except SignatureExpired:
    print("The token is expired")

print(os.environ.get('MAIL_USER'))
print(os.environ.get('MAIL_PASS'))   
 