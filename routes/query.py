from flask import session, abort, request, render_template
from . import routes
import utils.database


@routes.route("/query", methods=["POST"])
def query():
    if "user" not in session or "is_admin" not in session:
        abort(401)
    info = {}
    for item in request.form:
        if request.form[item] != "":
            info[item] = request.form[item]
    status, res = utils.database.queryTrain(utils.database.DBConn, info)
    if not status:
        return render_template("list.html", info={})
    else:
        return render_template("list.html", info=res)


@routes.route("/query_list", methods=["POST"])
def queryList():
    if "user" not in session or "is_admin" not in session:
        abort(401)
    info = {}
    for item in request.form:
        if request.form[item] != "":
            info[item] = request.form[item]
    status, res = utils.database.queryTrain(utils.database.DBConn, info)
    if not status:
        return render_template("list_button.html", info={})
    else:
        return render_template("list_button.html", info=res)
