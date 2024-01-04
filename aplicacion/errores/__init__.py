from flask import Blueprint

errores = Blueprint('errores', __name__, template_folder='templates')

from . import routes