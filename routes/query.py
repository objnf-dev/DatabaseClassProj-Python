from flask import session, abort, request, render_template
from . import routes
import utils.database


@routes.route("/api/query", methods=["POST"])
def query():
    if "user" not in session or "is_admin" not in session:
        abort(401)
    info = {}
    for item in request.form:
        if request.form[item] != "":
            info[item] = request.form[item]
    status, res = utils.database.queryTrain(utils.database.DBConn, info)
    if not status:
        abort(500)
    else:
        return render_template("list.html", info=res)


@routes.route("/api/query_list", methods=["POST"])
def queryList():
    if "user" not in session or "is_admin" not in session:
        abort(401)
    info = {}
    if "train_name" in request.form and request.form["train_name"]:
        info["train_name"] = request.form["train_name"]
    status, res = utils.database.queryTrain(utils.database.DBConn, info)
    if not status:
        abort(500)
    return render_template("list_button.html", info=res)


@routes.route("/api/query_user", methods=["GET"])
def queryUser():
    if "user" not in session or "is_admin" not in session:
        abort(401)
    status, res = utils.database.queryAllUser(utils.database.DBConn)
    if not status:
        abort(500)
    return render_template("userlist.html", data=res)


@routes.route("/api/query_order", methods=["GET"])
def queryOrder():
    if "user" not in session or "is_admin" not in session:
        abort(401)
    status, res = utils.database.queryOrder(utils.database.DBConn, session["user"])
    if not status:
        abort(500)
    return render_template("list_button.html", info=res)
