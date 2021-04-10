from flask import redirect, render_template, request, url_for, abort, session, flash, jsonify
from app.db import connection
from email_validator import validate_email, EmailNotValidError
import bcrypt
from app.models.house import House
from app.models.user import User
from app.helpers.auth import authenticated


def register():
    return render_template("user/register.html")


def login():
    email = request.form.get("email")
    password = request.form.get("password")
    if(email == None) or (email == ""):
        flash("Faltó ingresar el correo electrónico", category="error")
        return redirect(request.referrer)
    if(password == None) or (password == ""):
        flash("Faltó ingresar la contraseña", category="error")
        return redirect(request.referrer)
    
    try:
        validate_email(email)
        conn = connection()
        user = User.find_by_email(conn, email)
        if not user:
            flash("El correo no pertenece a ningún usuario", category="error")
            return redirect(request.referrer)
        else:
            if bcrypt.checkpw(password.encode('utf8'), user["password"].encode('utf8')):
                flash("Sesión iniciada!", category="success")
                session["user"] = user
                return redirect(request.referrer)
            else:
                flash("Usuario o contraseña inválido", category="error")
                return redirect(request.referrer)
    
    except EmailNotValidError:
        flash("El correo electrónico no es válido", category="error")
        return redirect(request.referrer)


def create():

    errors = False

    required_fields = ["email", "first_name", "last_name", "phone_number", "password1", "password2"]

    params = request.form

    for key in required_fields:
        if params[key] == "":
            
            translate_key = {
                "email": "Correo electrónico",
                "first_name": "Nombre", 
                "last_name": "Apellido",
                "phone_number": "Teléfono",
                "password1": "Contraseña", 
                "password2": "Repita la contraseña",
            }

            flash("Falta el campo '" + translate_key[key] + "'", category="error")
            errors = True

    if params["password1"] != params["password2"]:
        flash("Las contraseñas no coinciden", category="error")
        errors = True

    try:
        validate_email(params["email"])
        conn = connection()
        if User.find_by_email(conn, params["email"]):
            flash("Ya existe un usuario con ese correo", category="error")
            errors = True
    
    except EmailNotValidError:
        flash("El correo electrónico no es válido", category="error")
        errors = True
        
    if (not errors):
        user_dic = {
            "email": params["email"],
            "first_name": params["first_name"],
            "last_name": params["last_name"],
            "phone_number": params["phone_number"],
            "password": bcrypt.hashpw(params["password1"].encode('utf8'), bcrypt.gensalt()),
        }
        User.create(conn, user_dic)
        user = User.find_by_email(conn, user_dic["email"])
        session["user"] = user
        
        flash("Usuario creado", category="success")
        return redirect(url_for("index"))
    
    return redirect(request.referrer)

def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")
    return redirect(url_for("index"))


def favorite_houses():
    if not authenticated(session):
        abort(401)
    else:
        conn = connection()
        houses = User.favorite_houses(conn, session['user']['id'])
        return render_template("houses/all_houses.html", title="Tu lista de favoritos", houses=houses)

def add_fav_house():
    if not authenticated(session):
        abort(401)
    else:
        try:
            params = request.get_json()
            id_user = params['id_user']
            id_house = params['id_house']
            conn = connection()
            if(User.has_favorite(conn, id_user, id_house)):
                User.delete_fav_house(conn, id_user, id_house)
                return jsonify({"text": "deleted"})
            else:
                User.add_fav_house(conn, id_user, id_house)
                return jsonify({"text": "added"})
        except:
            abort(500)


def is_favorite(id_house):
    conn = connection()
    id_user = session['user']['id']
    return User.has_favorite(conn, id_user, id_house)


def houses_on_sale():
    if not authenticated(session):
        abort(401)
    conn = connection()
    houses = User.houses_on_sale(conn, session['user']['id'])
    return render_template("houses/all_houses.html", title="Tus publicaciones", houses=houses)


def buy_house():
    if not authenticated(session):
        abort(401)

    id_house = request.form.get("id_house")
    if (not id_house):
        flash("No hay una casa seleccionada")
        return redirect(request.referrer)
    conn = connection()
    if House.exist(conn, id_house):
        if User.buy_house(conn, session['user']['id'], id_house):
            flash("Compra exitosa", category="success")
        else:
            flash("Ha ocurrido un error", category="error")
    else:
        flash("No puedes comprar esta propiedad", category="error")
    return redirect(request.referrer)


def phone(id_user):
    conn = connection()
    phone = User.phone(conn, id_user)
    return phone["phone_number"]


def purchases():
    if not authenticated(session):
        abort(401)
    conn = connection()
    houses = House.purchases(conn, session['user']['id'])
    return render_template("houses/all_houses.html", title="Tus compras", houses=houses)


def is_owner(id_house):
    if not authenticated(session):
        abort(401)
    conn = connection()
    if (User.is_owner(conn, session['user']['id'], id_house)):
        return True
    return False