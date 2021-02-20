from flask import request, jsonify, Blueprint
from src.models.database import Data

histories = Blueprint('histories', __name__, template_folder='templates', static_folder='static')

data = Data() # Instanciando un objeto para utilizar las consultas a la db


@histories.route('/consult_history', methods=['POST'])
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


@histories.route('/add_history', methods=['POST'])
def add_history(): # Agregar registro al historial de un cliente
    description = request.form['description']
    payment_date = request.form['payment_date']
    payment = request.form['payment']
    id = request.form['id']
    data.RegistrarHistorial(description ,payment_date, payment, id)

    return jsonify({'message': 'successful operation'})


@histories.route('/update_history', methods=['POST'])
def update_history(): # Editar un registro del historial de un cliente
    history_id = request.form['history_id']
    description = request.form['description']
    payment_date = request.form['payment_date']
    payment = request.form['payment']
    data.ActualizarHistorial(history_id,description,payment_date,payment)

    return jsonify({'message': 'successful operation'})


@histories.route('/delete_history', methods=['POST'])
def delete_history(): # Eliminar un registro del historial de un cliente
    history_id = request.form['history_id']
    data.EliminarHistorial(history_id)

    return jsonify({'message': 'successful operation'})