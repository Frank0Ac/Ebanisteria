from flask import render_template
from . import acercade


@acercade.route('/acercade')
def acercade():
    #Página acercade
    return render_template('acercade.html')