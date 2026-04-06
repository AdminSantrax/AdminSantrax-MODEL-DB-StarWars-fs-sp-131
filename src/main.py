import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    db_url = db_url.replace("postgres://", "postgresql://")

app.config["SQLALCHEMY_DATABASE_URI"] = db_url if db_url else "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
Migrate(app, db)
CORS(app)
setup_admin(app)

CURRENT_USER_ID = 1


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route("/")
def sitemap():
    return generate_sitemap(app)


@app.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@app.route("/users/favorites", methods=["GET"])
def get_user_favorites():
    user = User.query.get(CURRENT_USER_ID)

    if user is None:
        return jsonify({"msg": "Usuario actual no encontrado"}), 404

    favorites = Favorite.query.filter_by(user_id=CURRENT_USER_ID).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200


@app.route("/people", methods=["GET"])
def get_all_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200


@app.route("/people/<int:people_id>", methods=["GET"])
def get_one_people(people_id):
    person = People.query.get(people_id)

    if person is None:
        return jsonify({"msg": "Personaje no encontrado"}), 404

    return jsonify(person.serialize()), 200


@app.route("/planets", methods=["GET"])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200


@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if planet is None:
        return jsonify({"msg": "Planeta no encontrado"}), 404

    return jsonify(planet.serialize()), 200


@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_people(people_id):
    user = User.query.get(CURRENT_USER_ID)
    person = People.query.get(people_id)

    if user is None:
        return jsonify({"msg": "Usuario actual no encontrado"}), 404

    if person is None:
        return jsonify({"msg": "Personaje no encontrado"}), 404

    existing_favorite = Favorite.query.filter_by(
        user_id=CURRENT_USER_ID,
        people_id=people_id
    ).first()

    if existing_favorite:
        return jsonify({"msg": "Ese personaje ya está en favoritos"}), 400

    new_favorite = Favorite(
        user_id=CURRENT_USER_ID,
        people_id=people_id
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({
        "msg": "Personaje añadido a favoritos",
        "favorite": new_favorite.serialize()
    }), 201


@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    user = User.query.get(CURRENT_USER_ID)
    planet = Planet.query.get(planet_id)

    if user is None:
        return jsonify({"msg": "Usuario actual no encontrado"}), 404

    if planet is None:
        return jsonify({"msg": "Planeta no encontrado"}), 404

    existing_favorite = Favorite.query.filter_by(
        user_id=CURRENT_USER_ID,
        planet_id=planet_id
    ).first()

    if existing_favorite:
        return jsonify({"msg": "Ese planeta ya está en favoritos"}), 400

    new_favorite = Favorite(
        user_id=CURRENT_USER_ID,
        planet_id=planet_id
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({
        "msg": "Planeta añadido a favoritos",
        "favorite": new_favorite.serialize()
    }), 201


@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_people(people_id):
    favorite = Favorite.query.filter_by(
        user_id=CURRENT_USER_ID,
        people_id=people_id
    ).first()

    if favorite is None:
        return jsonify({"msg": "Favorito de personaje no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Personaje eliminado de favoritos"}), 200


@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    favorite = Favorite.query.filter_by(
        user_id=CURRENT_USER_ID,
        planet_id=planet_id
    ).first()

    if favorite is None:
        return jsonify({"msg": "Favorito de planeta no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Planeta eliminado de favoritos"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3001))
    app.run(host="0.0.0.0", port=port, debug=True)