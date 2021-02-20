
# sessiones, login y contraseñas

from flask import request, url_for, session, redirect, flash, Blueprint
from src.models.database import Data

sessions = Blueprint('sessions',__name__, template_folder='templates', static_folder='static')

data = Data() # Instanciando un objeto para utilizar las consultas a la db


@sessions.before_request 
def session_management():
    session.permanent = True


@sessions.route('/consult_login', methods=['POST'])
def consult_login(): # Validar login
    user = request.form['user']
    password = request.form['password']

    validate = data.ConsultarLogin(user,password)
    if validate:
        session['user'] = user
        session.pop('_flashes', None)

    else: flash('Login incorrecto')

    return redirect(url_for('pages.index'))
    

@sessions.route('/update_password', methods=['POST'])
def update_password(): # Validar contraseña actual
    current_pass = request.form['current_pass']
    new_pass = request.form['new_pass']
    confirm_pass = request.form['confirm_pass']

    if data.ValidarContra(current_pass):
        if new_pass != confirm_pass:
            flash('No coinciden las nuevas contraseñas')
        else:
            data.ActualizarContra(new_pass) # Actualizar contraseña
            session.pop('_flashes', None) # Cerrar sessión
            return redirect(url_for('sessions.close_session')) # y volver a logearse
            
    else:
        flash('Contraseña actual incorrecta')

    return redirect(url_for('pages.change_password'))


@sessions.route('/close_session')
def close_session():
    session.clear()
    return redirect(url_for('pages.index'))