
from flask import render_template, request, url_for, session, redirect, Blueprint

pages = Blueprint('pages', __name__, template_folder='templates', static_folder='static')


@pages.app_errorhandler(404)
def page_not_found(err): # La pagina no existe
    return render_template('errors/404.html'), 404


@pages.app_errorhandler(405)
def method_not_allowed(err):
    return render_template('errors/405.html'), 405


@pages.app_errorhandler(500)
def server_problems(err):
    return render_template('errors/500.html'), 500


@pages.route('/')
def index(): # Ruta inicial
    if 'user' in session: return redirect(url_for('pages.clients'))
    else: return render_template('login.html')

@pages.route('/clients')
def clients(): # Ruta para la plantilla de clientes
    if 'user' in session: return render_template('clients.html')
    else: return redirect(url_for('pages.index'))


@pages.route('/history')
def history(): # Ruta para la plantilla de historiales
    if 'user' in session: return render_template('history.html')
    else: return redirect(url_for('pages.index'))


@pages.route('/change_password')
def change_password(): # Ruta para la plantilla de cambio de contraseña
    if 'user' in session: return render_template('change_password.html')
    else: return redirect(url_for('pages.index'))