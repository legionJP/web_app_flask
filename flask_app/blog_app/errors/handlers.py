from flask import Blueprint , render_template

errors = Blueprint('error',__name__)

#using the  route for the errors handlers

@errors.app_errorhandler(404)       #app_errorhandler will work for the enitre app not only for this blueprint
def error_404(error):
    return render_template('errors/404.html'),404

@errors.app_errorhandler(403)
def error_404(error):
    return render_template('errors/403.html'),403

@errors.app_errorhandler(500)
def error_404(error):
    return render_template('errors/500.html'),500





