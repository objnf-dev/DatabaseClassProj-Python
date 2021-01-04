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
    if "username" in request.form and request.form["username"] and "train" in request.form and request.form["train_name"]:
        status = utils.database.placeOrder(utils.database.DBConn, request.form["train_name"], request.form["username"])
        if status:
            return "ok"
        else:
            abort(500)
    else:
        abort(500)


@routes.route("/refund")
def refund():
    if "user" not in session or "is_admin" not in session:
        return redirect("/login")
    return render_template("refund.html")


@routes.route("/api/refund", methods=["POST"])
def rmOrder():
    pass