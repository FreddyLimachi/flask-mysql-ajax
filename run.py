
from flask import Flask

from routes.sessions import sessions
from routes.clients import clients
from routes.histories import histories
from routes.pages import pages


app = Flask(__name__)

app.secret_key = 'my_secret_key'

# Rutas para la sección de autenticaciones y contraseñas
app.register_blueprint(sessions)

# Rutas para la sección de paginas
app.register_blueprint(pages)

# Rutas para la sección de clientes
app.register_blueprint(clients)

# Rutas para la sección de historiales
app.register_blueprint(histories)


# Settings
debug = True

host = '0.0.0.0'

port = '5000'


if __name__ == "__main__":
    app.run(debug=debug, host=host, port=port)
