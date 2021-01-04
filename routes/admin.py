from flask import session, request, render_template, redirect, abort
from . import routes
import utils.database


@routes.route("/admin")
def admin():
    if "user" not in session or "is_admin" not in session:
        return redirect("/login")
    elif not session["is_admin"]:
        abort(401)
    return render_template("admin.html")


@routes.route("/change", methods=["POST"])
def change():
    if "user" not in session or "is_admin" not in session:
        abort(401)
    elif not session["is_admin"]:
        abort(401)
    info = {}
    return render_template("list_admin.html", info=info)