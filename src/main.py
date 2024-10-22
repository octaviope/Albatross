import argparse
import sys
import threading
import time
import signal

from ALBATROSS_protocol.Network_simulation.network_management.network import Network
from ALBATROSS_protocol.Network_simulation.network_communication.flask_server import FlaskServer
from ALBATROSS_protocol.albatross import Albatross

# Clase que redirige la salida tanto a archivo como a la terminal
class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w")

    def write(self, message):
        self.terminal.write(message)  # Imprimir en la terminal
        self.log.write(message)       # Guardar en el archivo

    def flush(self):
        pass


def signal_handler():
    print("Cerrando el servidor...")
    sys.exit(0)

# Comandos por terminal
def manage_terminal_input():
    # Capturar la señal Ctrl+C usando signal_handler
    signal.signal(signal.SIGINT, signal_handler)

    # Captura el número de participantes por terminal
    parser = argparse.ArgumentParser(description="Procesa dos números de entrada.")
    parser.add_argument('--n', type=int, default=512, help='Número de participantes.')
    args = parser.parse_args()
    if args.n < 1:
        print(f"Error: Número de participantes ({args.n}) es demasiado pequeño, se requieren al menos 100 participantes.")
        sys.exit(1)
    return args.n

# Crea la red
def create_network(num_participants):
    network = Network(num_participants)
    network.create_nodes()
    network.assign_neighbors()
    network.pk_to_ledger()
    return network

# Inicia el servidor
def start_flask_server(network):
    flask_server = FlaskServer(network)
    def run_server():
        flask_server.run()

    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(2)  # Dar tiempo al servidor para arrancar
    return server_thread

# Función principal
if __name__ == '__main__':
    # Redirigir salida estándar y errores tanto a un archivo log.txt como a la terminal
    sys.stdout = Logger("log.txt")
    sys.stderr = sys.stdout

    num_participants = manage_terminal_input()
    network = create_network(num_participants)

    start_flask_server(network)

    protocol = Albatross(network, num_participants)
    protocol.execute_commit_phase()
    protocol.execute_reveal_phase()
    protocol.handle_output_phase()

    # Mantener el hilo principal activo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Servidor detenido.")
