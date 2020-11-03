from flask import request, jsonify, Blueprint
from models.database import Data

clients = Blueprint('clients', __name__, template_folder='templates', static_folder='static')

data = Data() # Instanciando un objeto para utilizar las consultas a la db

@clients.route('/add_client', methods=['POST'])
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


@clients.route('/consult_client', methods=['POST'])
def consult_client():
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


@clients.route('/upload_client', methods=['POST'])
def upload_client():
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


@clients.route('/update_client', methods=['POST'])
def update_client():
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


@clients.route('/delete_client', methods=['POST'])
def delete_client():
    id = request.form['id']
    data.EliminarCliente(id)
    return jsonify({'message': 'successful operation'})


@clients.route('/search_client', methods=['POST'])
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


@clients.route('/update_status', methods=['POST'])
def update_status(): # editar estado de un cliente (activo, inactivo)
    id = request.form['id']
    status = request.form['status']
    status_date = request.form['status_date']
    data.ActualizarEstado(id,status,status_date)
    return jsonify({'message': 'successful operation'})