import os
from flask import current_app ,render_template, request, url_for, redirect, flash, session
from flask_mail import Message
from flask_babel import _
import sqlite3
from . import cuenta
from aplicacion.cuenta.forms import Formulariologin, Formularioregistro

def send_confirmation_email(email):
    from aplicacion import serializer, mail
    token = serializer.dumps(email, salt='email-confirm')
    confirmation_url = url_for('cuenta.confirm_email', token=token, _external=True)

    message = Message('Confirm your email', recipients=[email])
    message.body = f"Click the link to confirm your email: {confirmation_url}"

    try:
        mail.send(message)
    except Exception as e:
        print(f"Error sending email: {e}")

@cuenta.route('/login', methods=["GET", "POST"])
def login():

    # Check if the user is already logged in
    if 'user_id' in session:
        flash(_('You are already logged in'), 'info')
        return redirect(url_for('catalogo.pagina_catalogo'))

    form = Formulariologin(request.form)

    if form.validate_on_submit():
        username = form.usuariologin.data
        password = form.contrasenialogin.data

        print("Intentando acceder a la base de datos desde la ruta:", os.getcwd())

        conn = sqlite3.connect('aplicacion/database/ebanisteria.db')
        cursor = conn.cursor()

        # Buscar el usuario en la base de datos
        cursor.execute('SELECT * FROM User WHERE nom_usuario = ?', (username,))
        user = cursor.fetchone()

        if user and user[3] == 1 and user[4] == password:
            
            session['logged_in'] = True
            session['user_id'] = user[0]
            session['admin'] = user[5]
            session['username'] = user[1]

            flash(_('Inicio de sesión exitoso'), 'success')
            return redirect(url_for('catalogo.pagina_catalogo'))
        else:
            flash(_('Wrong username or password'), 'danger')

    return render_template('cuentalog.html', form=form)

@cuenta.route('/registro', methods=["GET", "POST"])
def registro():

    # Check if the user is already logged in
    if 'user_id' in session:
        flash(_('You are already logged in'), 'info')
        return redirect(url_for('catalogo.pagina_catalogo'))

    form = Formularioregistro(request.form)

    if form.validate_on_submit():
        usuarioreg = form.usuarioreg.data
        email = form.correoreg.data
        password = form.contraseniareg.data

        conn = sqlite3.connect('aplicacion/database/ebanisteria.db')
        cursor = conn.cursor()

        # Verificar si el usuario ya existe
        cursor.execute('SELECT * FROM User WHERE nom_usuario = ? OR correo = ?', (usuarioreg, email))
        existing_user = cursor.fetchone()

        if existing_user:
            flash(_('User or email already in use'), 'danger')
            conn.close()
        else:

            # Determine if this is the first user
            cursor.execute('SELECT COUNT(*) FROM User')
            user_count = cursor.fetchone()[0]

            # Set admin field based on user count
            admin = 1 if user_count == 0 else 0

            # Insert the user into the User table
            cursor.execute('INSERT INTO User (nom_usuario, correo, contrasenia, admin, verificado) VALUES (?, ?, ?, ?, ?)',
                           (usuarioreg, email, password, admin, 0))
            conn.commit()
            conn.close()

            send_confirmation_email(email)
            flash(_('Check your email for a confirmation link.'), 'success')
            return redirect(url_for("cuenta.login"))

    return render_template('registro.html', form=form)

@cuenta.route('/logout', methods=["POST"])
def logout():
    # Clear the user session
    session.clear()
    flash(_('Successfully logged out'), 'success')
    return redirect(url_for('catalogo.pagina_catalogo'))

@cuenta.route('/confirm/<token>')
def confirm_email(token):
    ruta = current_app.config['DATABASE_URI'].replace('sqlite:///', '')
    conexion = sqlite3.connect('aplicacion/database/ebanisteria.db')

    cursor = conexion.cursor()

    try:
        from aplicacion import serializer
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
        
        cursor.execute('SELECT * FROM User WHERE correo = ?', (email,))
        usuario = cursor.fetchone()

        if usuario:
            # Update the user's confirmation status
            cursor.execute('UPDATE User SET verificado = 1 WHERE id = ?', (usuario[0],))
            conexion.commit()

            flash(_('Email confirmed successfully!'), 'success')
        else:
            flash(_('User not found.'), 'danger')
    except:
        flash(_('The confirmation link is invalid or has expired.'), 'danger')
    finally:
        conexion.close()

    return redirect(url_for('cuenta.login'))