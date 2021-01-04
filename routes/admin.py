from flask import session, request, render_template, redirect, abort
from . import routes
import utils.database


@routes.route("/admin")
def admin():
    return render_template("admin.html")