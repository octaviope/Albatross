from flask import Flask
from ..network_communication.controller import NodeController

class FlaskServer:
    def __init__(self, network):
        self.app = Flask(__name__)  # Crear la aplicación Flask
        self.node_controller = NodeController(network)  # Instanciar el controlador de nodos con la red
        self.app.register_blueprint(self.node_controller.get_blueprint())

    def run(self, host="0.0.0.0", port=5000, debug=False):
        self.app.run(host=host, port=port, debug=debug)
