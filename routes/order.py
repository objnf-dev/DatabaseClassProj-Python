from flask import session, request, render_template, redirect, abort
from . import routes
import utils.database


@routes.route("/order")
def order():
    if "user" not in session or "is_admin" not in session:
        return redirect("/login")
    return render_template("order.html")


@routes.route("/api/order", methods=["POST"])
def placeOrder():
    if "user" not in session or "is_admin" not in session:
        abort(401)
    if "username" in request.form and request.form["username"] and "train_name" in request.form and \
            request.form["train_name"] and "status" in request.form and request.form["status"]:
        status = utils.database.placeOrder(utils.database.DBConn, request.form["username"], request.form["train_name"],
                                           request.form["status"])
        if status:
            return "ok"
        else:
            abort(500)
    else:
        abort(500)


@routes.route("/api/group_order", methods=["POST"])
def groupOrder():
    if "user" not in session or "is_admin" not in session:
        abort(401)
    if "username" in request.form and request.form["username"] and "train_name" in request.form and \
            request.form["train_name"] and "status" in request.form and request.form["status"]:
        nameList = request.form["username"].split(",")
        status = utils.database.placeGroupOrder(utils.database.DBConn, session["user"], nameList, \
                                                request.form["train_name"], request.form["status"])
        if status:
            return "ok"
    abort(500)


@routes.route("/refund")
def refund():
    if "user" not in session or "is_admin" not in session:
        return redirect("/login")
    return render_template("refund.html")


@routes.route("/api/refund", methods=["POST"])
def rmOrder():
    if "user" not in session or "is_admin" not in session:
        abort(401)
    if "oid" not in request.form or not request.form["oid"]:
        abort(500)
    status = utils.database.removeOrder(utils.database.DBConn, request.form["oid"], session["user"])
    if not status:
        abort(500)
    return "ok"


@routes.route("/api/group_refund", methods=["POST"])
def groupRmOrder():
    if "user" not in session or "is_admin" not in session:
        abort(401)
    if "oid" not in request.form or not request.form["oid"]:
        abort(500)
    status = utils.database.removeGroupOrder(utils.database.DBConn, request.form["oid"], session["user"])
    if not status:
        abort(500)
    return "ok"


@routes.route("/api/pay", methods=["POST"])
def payOrder():
    if "user" not in session or "is_admin" not in session:
        abort(401)
    if "oid" not in request.form or not request.form["oid"]:
        abort(500)
    status = utils.database.payOrder(utils.database.DBConn, request.form["oid"], session["user"])
    if not status:
        abort(500)
    return "ok"


@routes.route("/api/group_pay", methods=["POST"])
def payGroupOrder():
    if "user" not in session or "is_admin" not in session:
        abort(401)
    if "oid" not in request.form or not request.form["oid"]:
        abort(500)
    status = utils.database.groupPay(utils.database.DBConn, request.form["oid"], session["user"])
    if not status:
        abort(500)
    return "ok"
