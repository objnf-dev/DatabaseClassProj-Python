from flask import session, request, render_template, redirect, abort
from . import routes
import utils.database


# Homepage
@routes.route("/")
def index():
    if "user" not in session or "is_admin" not in session:
        return redirect("/login")
    return render_template("index.html")


# Login
@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "user" in session and "is_admin" in session:
            return "您已经登录。"
        return render_template("login.html")
    elif request.method == "POST":
        if "username" not in request.form or "password" not in request.form:
            abort(400)
        else:
            status, is_admin = utils.database.checkLogin(utils.database.DBConn, request.form["username"], request.form["password"])
            if status == False:
                abort(401)
            else:
                session["user"] = request.form["username"]
                session["is_admin"] = is_admin
                return "ok"


# Register
@routes.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "GET":
        if "user" in session:
            return "您已经登录，不能再注册。"
        return render_template("reg.html")
    elif request.method == "POST":
        if "username" not in request.form or "password" not in request.form:
            abort(400)
        elif not utils.database.checkUserUnique(utils.database.DBConn, request.form["username"]):
            abort(401)
        elif utils.database.createUser(utils.database.DBConn, request.form["username"], request.form["password"]):
            session["user"] = request.form["username"]
            session["is_admin"] = 0
            return "ok"
        else:
            abort(401)


# Logout
@routes.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("is_admin", None)
    return redirect("/login")
