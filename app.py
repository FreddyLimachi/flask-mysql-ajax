from flask import Flask, render_template, request, jsonify, url_for, redirect, flash
from database import Data
from datetime import date,datetime

app = Flask(__name__)

data = Data()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

## Rutas para la pagina principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/add_client', methods=['POST'])
def add_client():
    name = request.form['name']
    ip_adress = request.form['ip_adress']
    direc = request.form['direc']
    phone = request.form['phone']
    amount = request.form['amount']
    megas = request.form['megas']
    date = request.form['date']
    data.RegistrarCliente(name, ip_adress, direc, phone, amount, megas, date)
    rel_id=data.RelacionarCliente()
    data.RegistrarHistorial('Instalación',date,amount,rel_id)
    return 'Cliente agregado exitosamente'

@app.route('/consult_client', methods=['POST'])
def consult_client():
    response = data.ConsultarCliente()
    payload, content = [], {}
    for result in response:
        content = {'client_id': result[0], 'name': result[1],
                   'ip_adress': result[2], 'status': result[8]}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/upload_client', methods=['POST'])
def upload_client():
    client_id = request.form['client_id']
    response = data.CargarCliente(client_id)
    payload, content = [], {}
    for result in response:
        
        content = {'client_id': result[0], 'name': result[1],
                   'ip_adress': result[2], 'home_adress': result[3], 
                   'phone': result[4], 'month_payment': result[5],
                   'mbps': result[6], 'install_date': result[7]}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/edit_client', methods=['POST'])
def edit_client():
    client_id = request.form['client_id']

    name = request.form['name']
    ip_adress = request.form['ip_adress']
    direc = request.form['direc']
    phone = request.form['phone']
    amount = request.form['amount']
    megas = request.form['megas']
    date = request.form['date']
    data.ActualizarCliente(client_id,name,ip_adress,direc,phone,amount,megas,date)
    return 'registro actualizado exitosamente'

@app.route('/delete_client', methods=['POST'])
def delete_client():
    client_id = request.form['client_id']
    data.EliminarCliente(client_id,)
    return 'Cliente eliminado exitosamente'


## Rutas para la pagina de historiales

@app.route('/history')
def history():
    name=data.ConsultarCliente()
    time = date.today()  
    return render_template('history.html', client = name, time = time)

        
@app.route('/consult_history', methods=['POST'])
def consult_history():
    name_client=request.form['name']
    response = data.Upload_xname(name_client)
    for result in response:
        client_id=result[0]
    response = data.ConsultarHistorial(client_id)
    payload, content = [], {}
    for result in response:
        content = {'history_id': result[0], 'description': result[1],
                'date': result[2], 'payment': result[3]}
        payload.append(content)
        content = {}        
    return jsonify(payload)

@app.route('/add_history', methods=['POST'])
def add_history():
    name_client = request.form['name']
    year_month = request.form['year_month']
    payment = request.form['payment']
    payment_date = request.form['payment_date']
    
    dia=payment_date[8:10]
    mespago=payment_date[5:7]
    agepago=payment_date[0:4]

    payment_date2='{}/{}/{}'.format(dia,mespago,agepago)
    
    year=year_month[0:4]
    mes=int(year_month[5:7])-1
    
    ArregloMes=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    mes=ArregloMes[mes]

    response = data.Upload_xname(name_client)
    for result in response:
        client_id=result[0] 
    description = 'Pago {} {}'.format(mes,year)
    data.RegistrarHistorial(description ,payment_date2, payment, client_id)
    return 'Pago registrado exitosamente'


@app.route('/edit_history', methods=['POST'])
def edit_history():
    history_id = request.form['history_id']
    description = request.form['description']
    date_edit = request.form['date_edit']
    payment_edit = request.form['payment_edit']
    data.ActualizarHistorial(history_id,description,date_edit,payment_edit)
    return 'registro actualizado exitosamente'

@app.route('/delete_history', methods=['POST'])
def delete_history():
    history_id = request.form['history_id']
    print(history_id)
    data.EliminarHistorial(history_id)
    return 'Registro eliminado exitosamente'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')
