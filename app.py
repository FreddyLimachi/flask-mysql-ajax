from flask import Flask, render_template, request, jsonify, url_for, session, redirect, flash
from models.database import Data

app = Flask(__name__)
app.secret_key = 'my_secret_key'

data = Data() # Instanciando un objeto para utilizar las consultas a la db

@app.before_request 
def session_management():
    session.permanent = True


@app.errorhandler(404)
def page_not_found(e): # La pagina no existe
    return render_template('404.html'), 404


@app.route('/')
def index(): # Ruta inicial
    if 'user' in session:
        return render_template('clients.html')
    else:
        return render_template('login.html')


@app.route('/consult_login', methods=['POST'])
def consult_login(): # Validar login
    user = request.form['user']
    password = request.form['password']

    validate = data.ConsultarLogin(user,password)
    if validate:
        session['user'] = user
        session.pop('_flashes', None)

    else: flash('Login incorrecto')

    return redirect(url_for('index'))


@app.route('/change_password')
def change_password(): # Ruta para la plantilla de cambio de contraseña
    if 'user' in session:
        return render_template('change_password.html')
    else:
        return redirect(url_for('index'))
    

@app.route('/update_password', methods=['POST'])
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
            return redirect(url_for('close_session')) # y volver a logearse
            
    else:
        flash('Contraseña actual incorrecta')

    return redirect(url_for('change_password'))


@app.route('/close_session')
def close_session():
    session.clear()
    return redirect(url_for('index'))


@app.route('/add_client', methods=['POST'])
def add_client():
    name = request.form['name']
    ip_adress = request.form['ip_adress']
    home_adress = request.form['home_adress']
    phone = request.form['phone']
    month_payment= request.form['month_payment']
    mbps = request.form['mbps']
    install_date = request.form['install_date']
    data.RegistrarCliente(name, ip_adress, home_adress, phone, month_payment, mbps, install_date)
    last_id = data.UltimoCliente()
    data.RegistrarHistorial('Instalación',install_date,month_payment,last_id)
    return jsonify({'message': 'successful operation'})


@app.route('/consult_client', methods=['POST'])
def consult_client(): # Solicitar datos de clientes
    view = request.form['clients_view']
    order = request.form['order_ip']
    response = data.ConsultarCliente(view,order)
    payload, content = [], {}
    for result in response:
        content = {'id': result[0], 'name': result[1],
                   'ip_adress': result[2]}
        payload.append(content)
        content = {}
    return jsonify(payload)


@app.route('/upload_client', methods=['POST'])
def upload_client(): # Solicitar datos de un solo cliente
    id = request.form['id']
    response = data.CargarCliente(id)
    for result in response:
        content = {'id': result[0], 'name': result[1],
                   'ip_adress': result[2], 'home_adress': result[3], 
                   'phone': result[4], 'month_payment': result[5],
                   'mbps': result[6], 'install_date': result[7],
                   'status': result[8]}
    try:
        return jsonify(content)
    except UnboundLocalError:
        return jsonify({'month_payment': '0'})


@app.route('/edit_client', methods=['POST'])
def edit_client():
    id = request.form['id']
    name = request.form['name']
    ip_adress = request.form['ip_adress']
    home_adress = request.form['home_adress']
    phone = request.form['phone']
    month_payment = request.form['month_payment']
    mbps = request.form['mbps']
    install_date = request.form['install_date']
    data.ActualizarCliente(id,name,ip_adress,home_adress,phone,month_payment,mbps,install_date)
    return jsonify({'message': 'successful operation'})


@app.route('/delete_client', methods=['POST'])
def delete_client():
    id = request.form['id']
    data.EliminarCliente(id)
    return jsonify({'message': 'successful operation'})


@app.route('/edit_status', methods=['POST'])
def edit_status(): # editar estado de un cliente (activo, inactivo)
    id = request.form['id']
    status = request.form['status']
    status_date = request.form['status_date']
    data.ActualizarEstado(id,status,status_date)
    return jsonify({'message': 'successful operation'})


@app.route('/search_client', methods=['POST'])
def search_client():
    clients_view = request.form['clients_view']
    name = request.form['name']
    response = data.BuscarCliente(clients_view,name)
    payload, content = [], {}
    for result in response:
        content = {'id': result[0], 'name': result[1],
                   'ip_adress': result[2]}
        payload.append(content)
        content = {}
    return jsonify(payload)


## Rutas para la pagina de historiales
@app.route('/history')
def history():
    if 'user' in session:
        return render_template('history.html')
    else:
        return redirect(url_for('index'))


@app.route('/consult_history', methods=['POST'])
def consult_history(): # Solicitar historial de un cliente
    id = request.form['id']
    response = data.ConsultarHistorial(id)
    payload, content = [], {}
    for result in response:
        content = {'history_id': result[0], 'description': result[1],
                'payment_date': result[2], 'payment': result[3]}
        payload.append(content)
        content = {}      
    return jsonify(payload)


@app.route('/add_history', methods=['POST'])
def add_history(): # Agregar registro al historial de un cliente
    description = request.form['description']
    payment_date = request.form['payment_date']
    payment = request.form['payment']
    id = request.form['id']
    data.RegistrarHistorial(description ,payment_date, payment, id)
    return jsonify({'message': 'successful operation'})


@app.route('/edit_history', methods=['POST'])
def edit_history(): # Editar un registro del historial de un cliente
    history_id = request.form['history_id']
    description = request.form['description']
    payment_date = request.form['payment_date']
    payment = request.form['payment']
    data.ActualizarHistorial(history_id,description,payment_date,payment)
    return jsonify({'message': 'successful operation'})


@app.route('/delete_history', methods=['POST'])
def delete_history(): # Eliminar un registro del historial de un cliente
    history_id = request.form['history_id']
    data.EliminarHistorial(history_id)
    return jsonify({'message': 'successful operation'})
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')
