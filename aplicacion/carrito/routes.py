from flask import render_template, session, redirect, url_for, request, flash, current_app
from . import carrito
from aplicacion.database.crud_carrito import ver_carrito, remove_product, editar_cantidad, generate_pdf_bill, vaciar_carrito
from aplicacion.admin.forms import FormularioBorrar
from .forms import FormularioEditarCantidad, FormularioComprar
from flask_babel import _
from flask_mail import Message
import sqlite3

@carrito.route('/carrito', methods=['GET', 'POST'])
def pagina_carrito():
   if 'logged_in' not in session:
      return redirect(url_for('cuenta.login'))
   
   productos = ver_carrito(session['user_id'])
   form = FormularioEditarCantidad(request.form)
   formDp = FormularioBorrar(request.form)
   formBp = FormularioComprar(request.form)
   total_to_pay = 0

   for product in productos:
      total_to_pay += product[2]*product[3]

   if request.method == 'POST' and form.validate_on_submit():
      product_id = request.form.get('id')
      new_quantity_txt = request.form.get('cantidad')

      try:
        new_quantity = int(new_quantity_txt)
      except:
        flash(_('Invalid Quantity'))
        return redirect(url_for('carrito.pagina_carrito'))
       
      ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','')
      conexion=sqlite3.connect(ruta)

      cursor=conexion.cursor()
      cursor.execute('SELECT Productos.id, Productos.unidades FROM Productos WHERE id = ?', (product_id,))
      producto = cursor.fetchone()
      conexion.close()

      if new_quantity <= producto[1]:
        editar_cantidad(id=product_id, new_quantity=new_quantity)
      else:
        flash(_('Not enough units available'))
        
      return redirect(url_for('carrito.pagina_carrito'))

   return render_template('carrito.html', productos=productos, form=form, formDp=formDp, formBp=formBp, total_to_pay=total_to_pay)

@carrito.route('/delete_from_cart', methods=['POST'])
def quitar_producto():
   if 'logged_in' not in session:
      return redirect(url_for('cuenta.login'))
   
   product_id = request.form.get('id')
   remove_product(product_id)
   return redirect(url_for('carrito.pagina_carrito'))
   
@carrito.route('/buy_products', methods=['POST'])
def buy_products():
   if 'logged_in' not in session:
      return redirect(url_for('cuenta.login'))
   
   productos = ver_carrito(session['user_id'])
   total_to_pay = 0

   for product in productos:
      total_to_pay += product[2]*product[3]
   
   
   # Generate PDF bill
   pdf_buffer = generate_pdf_bill(productos, total_to_pay)

   from aplicacion import mail

   ruta=current_app.config['DATABASE_URI'].replace('sqlite:///','')
   conexion=sqlite3.connect(ruta)

   cursor=conexion.cursor()
   cursor.execute('SELECT User.id, User.correo FROM User WHERE id = ?', (session['user_id'],))
   usuario = cursor.fetchone()
   correo = usuario[1]

   # Send email with PDF attachment
   try:
      msg = Message('Your Invoice', recipients=[correo])
      msg.body = 'Thank you for your purchase!'
      msg.attach('invoice.pdf', 'application/pdf', pdf_buffer.read())

      mail.send(msg)

      vaciar_carrito(session['user_id'])
      flash(_('Purchase successful! Check your email for the invoice.'), 'success')
   except:
      flash(_('Error sending email. Please try again later.'), 'danger')
   finally:
      conexion.close()
      return redirect(url_for('carrito.pagina_carrito'))