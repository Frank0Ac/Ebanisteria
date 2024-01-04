from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_babel import _

class Formulariologin(FlaskForm): 
    usuariologin = StringField(_('Username'), validators=[DataRequired(_("User name required"))])
    contrasenialogin = PasswordField(_("Password"), validators=[DataRequired(_("Password required"))])
    submitlogin = SubmitField(_('Sign in'))

class Formularioregistro(FlaskForm): 
    usuarioreg = StringField(_('Username'), validators=[DataRequired(_("User name required"))])
    correoreg = StringField(_("E-mail"), validators=[DataRequired(_("E-mail required")),Email()])
    contraseniareg = PasswordField(_("Password"), validators=[DataRequired(_("Password required"))])
    submitreg = SubmitField(_('Sign up'))