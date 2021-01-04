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


@routes.route("/api/change", methods=["POST"])
def change():
    if "user" not in session or "is_admin" not in session:
        abort(401)
    elif not session["is_admin"]:
        abort(401)
    if "train_name" in request.form and "start_station" in request.form and "start_time" in request.form and "stop_station" \
        in request.form and "stop_time" in request.form and "price" in request.form and "capacity" in request.form and \
        "train_name_origin" in request.form and request.form["train_name"] and request.form["start_station"] and \
        request.form["start_time"] and request.form["stop_station"] and request.form["stop_time"] and request.form["price"] \
        and request.form["capacity"] and request.form["train_name_origin"]:
        trainInfo = [request.form["train_name"], request.form["start_station"], request.form["start_time"], \
                     request.form["stop_station"], request.form["stop_time"], request.form["price"], \
                     request.form["capacity"]]
        status = utils.database.updateTrain(utils.database.DBConn, trainInfo, request.form["train_name_origin"])
        if status:
            return "ok"
        else:
            abort(500)
    else:
        abort(500)


@routes.route("/api/create", methods=["POST"])
def create():
    if "user" not in session or "is_admin" not in session:
        abort(401)
    elif not session["is_admin"]:
        abort(401)
    if "train_name" in request.form and "start_station" in request.form and "start_time" in request.form and "stop_station" \
        in request.form and "stop_time" in request.form and "price" in request.form and "capacity" in request.form and \
        request.form["train_name"] and request.form["start_station"] and request.form["start_time"] and \
        request.form["stop_station"] and request.form["stop_time"] and request.form["price"] and request.form["capacity"]:

        trainInfo = [request.form["train_name"], request.form["start_station"], request.form["start_time"], \
                     request.form["stop_station"], request.form["stop_time"], request.form["price"], \
                     request.form["capacity"]]
        status = utils.database.createTrain(utils.database.DBConn, trainInfo)
        if status:
            return "ok"
        else:
            abort(500)
    else:
        abort(500)
