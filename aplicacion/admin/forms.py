from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, FileField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask import current_app
from flask_babel import _
import sqlite3

def get_opciones():
    ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','') # encontrol la url de la bd,replace quita sqlite(en que carpet se encutra la bd)
    conexion=sqlite3.connect(ruta)

    cursor=conexion.cursor()#para relizar consultas mediante un cursor
    cursor.execute('SELECT Tipos.id, Tipos.tipo FROM Tipos')
    opciones=cursor.fetchall()#fetchall varios productos-guardar productos de la consulta
    conexion.close()

    return opciones

class FormularioNuevoProducto(FlaskForm):
    nombre = StringField(_("User"), validators=[DataRequired(_("User name required"))])
    descripcion = StringField(_("Description"), validators=[DataRequired(_("Description required"))])
    cantidad = IntegerField(_("Available"), validators=[DataRequired(_('Quantity required')), NumberRange(min=1, message=_('Not valid quantity'))])
    costo = FloatField(_("Price"), validators=[DataRequired(_("Price required"))])
    imagen = FileField(_("Thumbanil"), validators=[DataRequired(_("Image required"))])
    tipo = SelectField(_("Type"), coerce=int, validators=[DataRequired(_("Type required"))])
    submit = SubmitField(_('Add product'))

    def __init__(self, *args, **kwargs):
        super(FormularioNuevoProducto, self).__init__(*args, **kwargs)
        self.tipo.choices = get_opciones()

class FormularioTipo(FlaskForm):
    nombre = StringField(_("Type name"), validators=[DataRequired(_("Name required"))])
    submit = SubmitField(_('Save'))

class FormularioEditarUsuario(FlaskForm):
    nombre = StringField(_("User name"))
    admin = BooleanField("Admin")
    submit = SubmitField(_('Save changes'))

class FormularioEditarProducto(FlaskForm):
    nombre = StringField(_("Product name"))
    descripcion = StringField(_("Description"))
    cantidad = IntegerField(_("Available"), validators=[NumberRange(min=1, message=_('Not valid quantity'))])
    costo = FloatField(_("Price"))
    tipo = SelectField(_("Type"), coerce=int, choices=get_opciones)
    img = FileField(_("Thumbnail"))
    submit = SubmitField(_('Save changes'))

class FormularioBorrar(FlaskForm):
    submit = SubmitField(_('Delete'))