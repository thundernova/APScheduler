from .login import *
from .admin_user import *
from .admin_userlog import *
from .admin_cron import *
from .admin_cronlog import *

def init_view(app):
    app.register_blueprint(blue_login)
    app.register_blueprint(blue_user)
    app.register_blueprint(blue_userlog)
    app.register_blueprint(blue_cron)
    app.register_blueprint(blue_cronlog)