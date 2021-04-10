from flask import redirect, render_template, request, url_for, abort, session, flash, jsonify
from app.db import connection
from app.models.house import House
from app.models.user import User
from app.helpers.auth import authenticated


def all():
    conn = connection()
    last_houses = House.last(conn)
    on_sale_houses = House.last_on_sale(conn)
    return render_template("index.html", last_houses=last_houses, on_sale_houses=on_sale_houses)


def show():
    id = request.args.get("id")
    if id is not None:
        conn = connection()
        house = House.find_by_id(conn, id)
        if house:
            if house["deleted_at"] is not None:
                if authenticated(session):
                    if User.bought_house(conn, house['id'], session['user']['id']):
                        return render_template("houses/show_house.html", house=house)
                    else:
                        abort(404)
                else:
                    abort(401)
            else:
                return render_template("houses/show_house.html", house=house)

        else:
            abort(404)
    else:
        abort(404)

def show_all_houses():
    conn = connection()
    all_houses = House.all(conn)
    return render_template("houses/all_houses.html", title="Todas las propiedades", houses=all_houses)

def show_sales():
    conn = connection()
    sales = House.on_sale(conn)
    return render_template("houses/all_houses.html", title="Las mejores ofertas!", houses=sales)


def update_stars(conn, id_house):
    likes = House.likes(conn, id_house)
    dislikes = House.dislikes(conn, id_house)
    likes = likes['likes']
    dislikes = dislikes['dislikes']
    try:
        rating = likes / (likes + dislikes)
        if rating <= 0.2:
            stars = 1
        if rating > 0.2:
            stars = 2
        if rating > 0.4:
            stars = 3
        if rating > 0.6:
            stars = 4
        if rating > 0.8:
            stars = 5
    except ZeroDivisionError:
        stars = None
        
    if stars is not None:
        House.update_stars(conn, id_house, stars)
    else:
        House.update_stars(conn, id_house, 0)

    return stars


def add_like():
    data = request.get_json()
    id_user = data['id_user']
    id_house = data['id_house']
    
    if(id_user == "" or id_user == None):
        abort(404)
    if(id_house == "" or id_house == None):
        abort(404)

    conn = connection()

    #Verify if the user or house exist
    if not User.find_by_id(conn, id_user):
        abort(404)
    if not House.find_by_id(conn, id_house):
        abort(404)
    if House.was_sold(conn, id_house):
        abort(404)

    #If the user has liked the house before
    if (House.verify_like(conn, id_user, id_house)):
        House.remove_like(conn, id_user, id_house)
    else:
        #If the user has disliked the house before
        if (House.verify_dislike(conn, id_user, id_house)):
            House.remove_dislike(conn, id_user, id_house)
        House.add_like(conn, id_user, id_house)

    stars = update_stars(conn, id_house)
    return jsonify({"likes": House.likes(conn, id_house), "dislikes": House.dislikes(conn, id_house), "stars": stars})
    

def add_dislike():
    data = request.get_json()
    id_user = data['id_user']
    id_house = data['id_house']
    
    if(id_user == "" or id_user == None):
        abort(404)
    if(id_house == "" or id_house == None):
        abort(404)
    conn = connection()
    if House.was_sold(conn, id_house):
        abort(404)

    #Verify if the user or house exist
    if not User.find_by_id(conn, id_user):
        abort(404)
    if not House.find_by_id(conn, id_house):
        abort(404)

    #If the user has disliked the house before
    if (House.verify_dislike(conn, id_user, id_house)):
        House.remove_dislike(conn, id_user, id_house)
    else:
        #If the user has liked the house before
        if (House.verify_like(conn, id_user, id_house)):
            House.remove_like(conn, id_user, id_house)
        House.add_dislike(conn, id_user, id_house)

    stars = update_stars(conn, id_house)
    return jsonify({"likes": House.likes(conn, id_house), "dislikes": House.dislikes(conn, id_house), "stars": stars})


def add_house():
    return render_template("houses/add_house.html")


def create_house():

    errors = False

    id_user = request.form.get("id_user")
    name = request.form.get("name")
    adress = request.form.get("adress")
    on_sale = request.form.get("on_sale")
    actual_price = request.form.get("actual_price")
    old_price = request.form.get("old_price")
    description = request.form.get("description")
    

    if(id_user is None)or(id_user == ""):
        flash("No se encuentra el nombre de usuario", category="error")
        errors = True

    if(name is None)or(name == ""):
        flash("La propiedad debe tener un nombre", category="error")
        errors = True

    if(adress is None)or(adress == ""):
        flash("La propiedad debe tener una dirección", category="error")
        errors = True

    if(on_sale is not None)and(on_sale):
        sale_is_ok = True
        if (actual_price is None) or (actual_price == ""):
            flash("Falta el precio actual!", category="error")
            errors = True
            sale_is_ok = False
        if (old_price is None) or (old_price == ""):
            flash("Falta el precio anterior!", category="error")
            errors = True
            sale_is_ok = False
        if sale_is_ok:
            if int(actual_price) >= int(old_price):
                flash("El precio actual debe ser más económico!", category="error")
                errors = True
    else:
        on_sale = False

    has_picture = 0

    for file in request.files.getlist("photo"):

        if file.filename != "":
            if "." in file.filename:
                ext = file.filename.split(".")[1].lower()
                if ext in ['png', 'jpg', 'jpeg', 'gif']:
                    has_picture = has_picture + 1
                else:
                    flash("El formato de las imágenes debe ser .png .jpg .jpeg o .gif!", category="error")
                    errors = True
            else:
                flash("El formato de las imágenes debe ser .png .jpg .jpeg o .gif!", category="error")
                errors = True

    
    if not errors:

        conn = connection()

        if on_sale:
            id_house = House.add_house(conn, id_user, name, adress, description, has_picture, actual_price, old_price, on_sale=1)
        else:
            if(actual_price is not None)and(actual_price != ""):
                id_house = House.add_house(conn, id_user, name, adress, description, has_picture, actual_price)
            else:
                id_house = House.add_house(conn, id_user, name, adress, description, has_picture)

        if has_picture > 0:
            picture_number = 1
            for file in request.files.getlist("photo"):
                file.save("./app/static/uploads/foto-casa-"+str(id_house)+"-"+str(picture_number))
                picture_number = picture_number + 1
        flash("Propiedad agregada!", category="success")
            
    return redirect(request.referrer)
        

def was_sold(id_house):
    conn = connection()
    return House.was_sold(conn, id_house)


def delete_house():
    if not authenticated(session):
        abort(401)
    id_house = request.form.get("id_house")

    if(id_house is None)or(id_house == ""):
        flash("La propiedad debe tener un ID", category="error")    
    else:
        conn = connection()
        if not User.is_owner(conn, session['user']['id'], id_house):
            flash("Solo el dueño de la publicación puede borrarla!", category="error")
        else:
            if House.was_sold(conn,id_house):
                flash("No puede eliminar una propiedad vendida!", category="error")
            else:
                House.delete(conn, id_house)
                flash("Se ha eliminado la publicación exitosamente!", category="success")
                return redirect(url_for("index"))
    
    return redirect(request.referrer)
    