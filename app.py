import random
from flask import Flask, request, jsonify
from node import Node
from ledger import PublicLedger
from Funciones import Funciones
import threading

app = Flask(__name__)
nodes = []

@app.route('/node/<int:node_id>/execute_protocol')
def execute_protocol(node_id):
    if nodes[node_id] != None:
        return nodes[node_id].execute_protocol()
    else:
        return f"Nodo {node_id} no encontrado", 404

@app.route('/node/<int:node_id>/get_invsk')
def get_invsk(node_id):
    if nodes[node_id] != None:
        return {'invsk': nodes[node_id].get_invsk()}
    else:
        return f"Nodo {node_id} no encontrado", 404


if __name__ == '__main__':
    # Creación de 1024 nodos
    n = 128
    size = 1024
    k = 128
    q, p = Funciones.findprime(k, size-k)
    h = pow(Funciones.generator(p), 2, p) 
    sk = []
    pk = []
    for i in range(n):
        sk.append(random.randint(0, q - 1))
        pk.append(pow(h, sk[i], p))
        nodes.append(Node(i, sk[i], pk, n, q, p, h))
    # Ejecución de la aplicación Flask
    app.run()
