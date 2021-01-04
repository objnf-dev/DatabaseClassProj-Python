from flask import session, request, render_template, redirect, abort
from . import routes
import utils.database


@routes.route("/order")
def order():
    return render_template("order.html")


@routes.route("/refund")
def refund():
    return render_template("refund.html")