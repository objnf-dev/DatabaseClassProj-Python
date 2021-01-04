from flask import Blueprint
routes = Blueprint('routes', __name__)


from .index import *
from .admin import *
from .query import *
from .order import *
