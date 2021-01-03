from flask import session, request, redirect, abort
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
        abort(500)
    else:
        return res
