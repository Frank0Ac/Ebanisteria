from flask import render_template
from . import errores
from flask_babel import _

@errores.app_errorhandler(404)
def page_not_found(error):
    return (render_template("error.html", error=_("Page not found...")),404)
@errores.app_errorhandler(403)
def forbidden(err):
    return (render_template("unforbidden.html"),403)
@errores.app_errorhandler(500)
def server_error(error):
    return (render_template("error500.html", error=_("Server error ...")),500)  