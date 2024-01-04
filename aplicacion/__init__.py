from flask import Flask, request
from flask_babel import Babel
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
import os
from .catalogo import catalogo
from .inicio import inicio
from .carrito import carrito
from .cuenta import cuenta
from .errores import errores
from .admin import admin

def get_locale():
    print(request.accept_languages)
    return request.accept_languages.best_match(app.config['LANGUAGES'])

app = Flask(__name__)
app.config.from_pyfile('config/configuracion.cfg')

babel = Babel(app=app, locale_selector=get_locale)

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Check if the upload folder exists, create it if not
upload_folder = app.config['UPLOAD_FOLDER']
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

app.register_blueprint(catalogo)
app.register_blueprint(inicio)
app.register_blueprint(carrito)
app.register_blueprint(cuenta)
app.register_blueprint(errores)
app.register_blueprint(admin)