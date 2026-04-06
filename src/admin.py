import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User, People, Planet, Favorite


class DefaultModelView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False


class FavoriteAdmin(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = ("id", "user", "people", "planet")
    form_columns = ("user", "people", "planet")


def setup_admin(app):
    app.secret_key = os.environ.get("FLASK_APP_KEY", "sample key")
    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
    admin = Admin(app, name="4Geeks Admin", template_mode="bootstrap3")

    admin.add_view(DefaultModelView(User, db.session))
    admin.add_view(DefaultModelView(People, db.session))
    admin.add_view(DefaultModelView(Planet, db.session))
    admin.add_view(FavoriteAdmin(Favorite, db.session))