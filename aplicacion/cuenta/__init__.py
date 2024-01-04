from flask import Blueprint

cuenta = Blueprint('cuenta', __name__, template_folder='templates', static_folder='static/css')

from . import routes