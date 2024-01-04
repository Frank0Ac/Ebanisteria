from flask import abort, render_template, flash, redirect, url_for, current_app, request, session
from . import catalogo
from .forms import FormularioComprarProducto
from aplicacion.database.crud_productos import obtenerproductos
from aplicacion.database.crud_carrito import agregar_al_carrito
from flask_babel import _
import sqlite3

@catalogo.route('/catalogo', methods=['GET', 'POST'])
def pagina_catalogo():
  
  page = request.args.get('page', 1, type=int)
  per_page = 3  # Adjust as needed
  productos, total_productos = obtenerproductos(page, per_page)

  form = FormularioComprarProducto(request.form)

  if form.validate_on_submit():
    product_id = request.form.get('id')
    cantidad_txt = request.form.get('cantidad')

    try:
      cantidad = int(cantidad_txt)
    except:
      flash(_('Invalid Quantity'))
      return redirect(url_for('catalogo.pagina_catalogo'))
       
    ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','')
    conexion=sqlite3.connect(ruta)

    cursor=conexion.cursor()
    cursor.execute('SELECT Productos.id, Productos.unidades FROM Productos WHERE id = ?', (product_id,))
    producto = cursor.fetchone()
    conexion.close()

    if 'user_id' in session and 'logged_in' in session and session['logged_in'] and cantidad <= producto[1]:
      agregar_al_carrito(user_id=session['user_id'], product_id=product_id, cantidad=cantidad)
      return redirect(url_for('carrito.pagina_carrito'))
    else:
      flash(_('Sorry, we could not add the product to your cart'))
      return redirect(url_for('catalogo.pagina_catalogo'))

  return render_template('catalogo.html', productos=productos, total_productos = total_productos, per_page=per_page, form=form)
    