from flask import Blueprint

acercade= Blueprint('acercade', __name__, template_folder='templates', static_folder='static/css')

from . import routes