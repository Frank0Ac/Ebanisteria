from flask import render_template
from . import inicio


@inicio.route('/')
def inicio():
    #Página Inicio
    return render_template('inicio.html')