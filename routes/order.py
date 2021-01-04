from flask import session, request, render_template, redirect, abort
from . import routes
import utils.database


@routes.route("/order")
def order():
    if "user" not in session or "is_admin" not in session:
        return redirect("/login")
    return render_template("order.html")


@routes.route("/placeOrder", methods=["POST"])
def placeOrder():
    if "user" not in session or "is_admin" not in session:
        abort(401)
    info = {}
    return render_template("list_button.html", info=info)


@routes.route("/refund")
def refund():
    if "user" not in session or "is_admin" not in session:
        return redirect("/login")
    return render_template("refund.html")