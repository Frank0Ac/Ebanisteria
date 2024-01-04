import os
from flask import render_template, request, url_for, redirect, flash, abort, session
from flask_babel import _
from . import admin
from aplicacion.admin.forms import FormularioNuevoProducto, FormularioTipo, FormularioEditarProducto, FormularioEditarUsuario, FormularioBorrar
from aplicacion.database.crud_usuarios import obtener_usuarios, editar_usuario, borrar_usuario
from aplicacion.database.crud_productos import obtenerproductos, obtener_tipos, crear_tipo, crear_producto, borrar_producto, editar_producto, borrar_tipo, editar_tipo
from werkzeug.utils import secure_filename

@admin.route('/admin', methods=["GET", "POST"])
def admin_page():

    if(('logged_in' not in session) or ('admin' in session and session['admin'] != 1)):
        abort(403, _('You are not allowed to access here'))

    page = request.args.get('page', 1, type=int)
    active_tab = request.args.get('active_tab', 'nuevoProductoTab')
    per_page = 3  # Adjust as needed
    usuarios, total_usuarios = obtener_usuarios(page, per_page)
    productos, total_productos = obtenerproductos(page, per_page)
    tipos = obtener_tipos()
    
    formNp = FormularioNuevoProducto(request.form)
    formNt = FormularioTipo(request.form)

    formEt = FormularioTipo(request.form)
    formEu = FormularioEditarUsuario(request.form)
    formEp = FormularioEditarProducto(request.form)

    formDu = FormularioBorrar(request.form)
    formDp = FormularioBorrar(request.form)
    formDt = FormularioBorrar(request.form)

    if request.method == 'POST':
        
        if formNt.validate_on_submit():
            nombre = request.form.get('nombre')
            crear_tipo(nombre)
            flash(_('New type successfully created'), 'success')
            return redirect(url_for('admin.admin_page'))

    return render_template('admin.html', formDu=formDu, formDp=formDp, formDt=formDt, formNp=formNp, formNt=formNt, formEt=formEt, formEu=formEu, formEp=formEp, tipos=tipos, productos=productos, total_productos= total_productos, usuarios=usuarios, total_usuarios=total_usuarios, per_page=per_page, active_tab=active_tab)

@admin.route('/nuevo_producto', methods=["POST"])
def nuevo_producto():
    nombre = request.form.get('nombre')
    tipo = request.form.get('tipo')
    cantidad_txt = request.form.get('cantidad')
    desc = request.form.get('descripcion')
    costo = request.form.get('costo')
    img = request.files['imagen']

    if img.filename != '':
        # Secure the filename to prevent potential security issues
        filename = secure_filename(img.filename)
        # Save the file to the desired directory (replace 'uploads' with your actual directory)
        from aplicacion import app
        try:
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except:
            flash(_('Error saving file'))
            return redirect(url_for('admin.admin_page'))
    else:
        # Handle the case where no file is selected (optional)
        flash(_('No image selected'), 'warning')
        return redirect(url_for('admin.admin_page'))
    
    try:
        cantidad = int(cantidad_txt)
        cantidad = cantidad if cantidad > 0 else 0
    except:
        flash(_('Cantidad no valida'), 'danger')
        return redirect(url_for('admin.admin_page'))

    crear_producto(nombre=nombre, cantidad=cantidad, tipo=tipo, costo=costo, desc=desc, img=filename)
    flash(_('New product successfully created'), 'success')
    return redirect(url_for('admin.admin_page'))

@admin.route('/edit_user', methods=['POST'])
def edit_user():
    user_id = request.form.get('id')
    nom_usuario = request.form.get('nombre')
    admin = 1 if request.form.get('admin') else 0

    if nom_usuario.__len__() < 3:
        editar_usuario(user_id = user_id, admin= admin)
    else:
        editar_usuario(user_id = user_id, nom_usuario = nom_usuario, admin= admin)
    flash(_('User successfully edited'), 'success')
    return redirect(url_for('admin.admin_page', active_tab='editarUsuarioTab'))

@admin.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form.get('id')
    borrar_usuario(user_id)
    flash(_('User successfully deleted'), 'success')
    return redirect(url_for('admin.admin_page', active_tab='editarUsuarioTab'))

@admin.route('/edit_product', methods=['POST'])
def edit_product():
    product_id = request.form.get('id')
    nombre = request.form.get('nombre')
    tipo = request.form.get('tipo')
    costo_txt = request.form.get('costo')
    desc = request.form.get('descripcion')
    img = request.files['img']

    nombre = nombre if nombre.__len__() >= 3 else None
    desc = desc if desc.__len__() >= 3 else None

    try:
        costo = float(costo_txt) if costo_txt.__len__() > 0 else None
    except:
        flash(_('Error editing price'))
        return redirect(url_for('admin.admin_page', active_tab='editarProductoTab'))

    if img and img.filename != '':
        # Secure the filename to prevent potential security issues
        filename = secure_filename(img.filename)
        # Save the file to the desired directory (replace 'uploads' with your actual directory)
        from aplicacion import app
        try:
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except:
            flash(_('Error saving file'))
            return redirect(url_for('admin.admin_page', active_tab='editarProductoTab'))
        editar_producto(product_id=product_id, nombre=nombre, tipo=tipo, costo=costo, desc=desc, img=filename)
    else:
        editar_producto(product_id=product_id, nombre=nombre, tipo=tipo, costo=costo, desc=desc)
    flash(_('Product successfully edited'), 'success')
    return redirect(url_for('admin.admin_page', active_tab='editarProductoTab'))

@admin.route('/delete_product', methods={'POST'})
def delete_product():
    product_id = request.form.get('id')
    borrar_producto(product_id)
    flash(_('Product successfully deleted'), 'success')
    return redirect(url_for('admin.admin_page', active_tab='editarProductoTab'))

@admin.route('/edit_type', methods=['POST'])
def edit_type():
    type_id = request.form.get('id')
    tipo = request.form.get('nombre')

    editar_tipo(type_id=type_id, tipo=tipo)
    flash(_('Typy successfully edited'), 'success')
    return redirect(url_for('admin.admin_page', active_tab='nuevoTipoTab'))

@admin.route('/borrar_tipo', methods={'POST'})
def delete_type():
    type_id = request.form.get('id')
    borrar_tipo(type_id)
    flash(_('Type successfully deleted'), 'success')
    return redirect(url_for('admin.admin_page', active_tab='nuevoTipoTab'))