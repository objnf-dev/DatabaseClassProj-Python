from flask import session, request, redirect, abort
from . import routes
import utils.database


@routes.route("/queryTrain", methods=["POST"])
def queryTrain():
    pass