from flask import Flask
from .config import config
from .exts import init_ext
from .views import init_view

def create_app(config_name):
    my_app = Flask(__name__,template_folder="templates",static_folder="static")
    my_app.config.from_object(config[config_name])
    config[config_name].init_app(my_app)
    init_ext(my_app)
    init_view(my_app)
    return my_app
