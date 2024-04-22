#importing app which is importing from __init__.py so  the app var should be in init.py

from blog_app import app
if __name__ == '__main__':
    app.run(debug=True) # it is equal to set DEBUG = 1
