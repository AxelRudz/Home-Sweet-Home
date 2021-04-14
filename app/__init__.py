from os import path, environ
from flask import Flask, render_template, g
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config
from app import db
from app.resources import house
from app.resources import user
from app.helpers import handler
from app.helpers import auth as helper_auth


def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # CSRF
    csrf = CSRFProtect(app)

    # Directory where pics are uploaded
    UPLOAD_FOLDER = './app/static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


    # Configure db
    db.init_app(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(is_favorite=user.is_favorite)
    app.jinja_env.globals.update(phone=user.phone)
    app.jinja_env.globals.update(was_sold=house.was_sold)
    app.jinja_env.globals.update(user_is_owner=user.is_owner)

    # Ruta para el Home
    app.add_url_rule("/", "index", house.all)

    # Houses routes
    app.add_url_rule("/show-house", "show_house", house.show)
    app.add_url_rule("/add-house", "add_house", house.add_house)
    app.add_url_rule("/delete-house", "delete_house", house.delete_house, methods=["POST"])
    app.add_url_rule("/create-house", "create_house", house.create_house, methods=["POST"])
    app.add_url_rule("/show-houses", "show_all_houses", house.show_all_houses)
    app.add_url_rule("/show-sales", "show_sales", house.show_sales)
    app.add_url_rule("/add-like", "add_like", house.add_like, methods=["POST"])
    app.add_url_rule("/add-dislike", "add_dislike", house.add_dislike, methods=["POST"])
    app.add_url_rule("/restore-houses", "restore_houses", house.restore_houses)

    # User routes
    app.add_url_rule("/user-register", "user_register", user.register)
    app.add_url_rule("/user-logout", "user_logout", user.logout)
    app.add_url_rule("/user-login", "user_login", user.login, methods=["POST"])
    app.add_url_rule("/user-create", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/user-favorite-houses", "user_favorite_houses", user.favorite_houses, methods=["GET"])
    app.add_url_rule("/user-houses-on-sale", "user_houses_on_sale", user.houses_on_sale, methods=["GET"])
    app.add_url_rule("/add-fav-house", "add_fav_house", user.add_fav_house, methods=["POST"])
    app.add_url_rule("/buy-house", "buy_house", user.buy_house, methods=["POST"])
    app.add_url_rule("/user-purchases", "user_purchases", user.purchases, methods=["GET"])
    
    # Retornar la instancia de app configurada
    return app
