from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_babel import _

class FormularioComprarProducto(FlaskForm):
    cantidad = IntegerField(_('Units'), validators=[DataRequired(_('How many do you want?')), NumberRange(min=1, message=_('Not valid quantity'))])
    submit = SubmitField(_('Add to cart'))