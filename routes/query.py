from flask import session, request, render_template
from . import routes
import utils.database


@routes.route("/query", methods=["POST"])
def queryTrain():
    info = {}
    for item in request.form:
        if request.form[item] != "":
            info[item] = request.form[item]
    status, res = utils.database.queryTrain(utils.database.DBConn, info)
    if not status:
        return render_template("list.html", info={})
    else:
        return render_template("list.html", info=res)
