

# Sign a user ID in a URL and email it to them to unsubscribe from a newsletter. 
# This way you don’t need to generate one-time tokens and store them in the database.
# Same thing with any kind of activation link for accounts and similar things.

from itsdangerous import URLSafeTimedSerializer,SignatureExpired
s= URLSafeTimedSerializer('secret')
token = s.dumps({'user_id':1},salt='verification')
try:
    data = s.loads(token,max_age=60)
    print(data)   #gives the data payload
    token_utf8 = token.decode('utf-8')
    print(token_utf8)
except:
    SignatureExpired
    print("The token is expired")