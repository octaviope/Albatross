from flask import Blueprint, jsonify, request
from ..network_management.node import Node
from ..network_management.network import Network

class NodeController:
    def __init__(self, network):
        self.controller = Blueprint('controller', __name__)  
        self.network: Network = network
        self.nodes: list[Node] = self.network.get_nodes()
        self.register_routes()
 
    # Endpoints
    def register_routes(self):

        @self.controller.route('/node/<int:node_id>/commit')
        def commit(node_id):
            if node_id < len(self.nodes) and self.nodes[node_id] is not None:
                result = self.nodes[node_id].commit()
                return result
            else:
                return f"Nodo {node_id} no encontrado", 404  
        
        
        @self.controller.route('/node/<int:node_id>/reveal')
        def reveal(node_id):
            if node_id < len(self.nodes) and self.nodes[node_id] is not None:
                result = self.nodes[node_id].reveal()
                return result
            else:
                return f"Nodo {node_id} no encontrado", 404  
            

        @self.controller.route('/node/<int:node_id>/output')
        def output(node_id):
            if node_id < len(self.nodes) and self.nodes[node_id] is not None:
                result = self.nodes[node_id].output()
                if result == False:
                    return {"status": "failure", "node": node_id}, 500
                else:
                    return {"result": result}, 200  # Devuelve el resultado como JSON
            else:
                return f"Nodo {node_id} no encontrado", 404
        

        @self.controller.route('/node/<int:node_id>/recovery')
        def recovery(node_id):
            # Obtiene los failed_nodes desde los parámetros de la URL
            failed_nodes = request.args.get('failed_nodes', '').split(',')
            failed_nodes = [int(node) for node in failed_nodes if node]  # Convierte a lista de enteros
            
            if node_id < len(self.nodes) and self.nodes[node_id] is not None:
                result = self.nodes[node_id].recovery(failed_nodes)  # Pasa failed_nodes a la función recovery
                if result == False:
                    return {"status": "failure", "node": node_id}, 500
                else:
                    return {"result": result}, 200 
            else:
                return f"Nodo {node_id} no encontrado", 404
        
        
        @self.controller.route('/node/<int:node_id>/reconstruction/<int:reco_id>')
        def reconstruction(node_id, reco_id):
            # Obtén los reco_parties desde los parámetros de la consulta
            reco_parties = request.args.get('reco_parties', '').split(',')
            reco_parties = [int(node) for node in reco_parties if node]  # Convierte a lista de enteros

            
            if reco_id < len(self.nodes) and self.nodes[reco_id] is not None:
                node = self.nodes[reco_id]
                # Pasa node_id y reco_parties a la función de reconstrucción del nodo
                result = node.reconstruction(node_id, reco_parties)
                
                if result is False:
                    return jsonify({"status": "failure", "node": node_id}), 500
                else:
                    return jsonify({"result": result}), 200
            else:
                return jsonify({"status": "error", "message": f"Nodo {node_id} no encontrado"}), 404




        @self.controller.route('/node/<int:node_id>/decrypt_fragment')
        def decrypt_fragment(node_id):
            i = request.args.get('i')  # Obtener el parámetro 'i' de la URL
            if i is not None:
                i = int(i)  # Convertir 'i' a entero
            if node_id < len(self.nodes) and self.nodes[node_id] is not None:
                self.nodes[node_id].decrypt_fragment(i)
                return jsonify({"status": "success", "message": f"Fragmento {i} desencriptado y subido al ledger."})
            else:
                return jsonify({"status": "error", "message": f"Nodo {node_id} no encontrado"}), 404


        @self.controller.route('/node/<int:node_id>/verify_lde/<int:ledger_id>')
        def verify_lde(node_id, ledger_id):
            if node_id < len(self.nodes) and self.nodes[node_id] is not None:
                node = self.nodes[node_id]
                if node.verifie_LDEI(ledger_id):
                    return jsonify({"status": "success", "message": "LDEI verificado correctamente"}), 200
                else:
                    return jsonify({"status": "error", "message": "LDEI incorrecto"}), 400
            return jsonify({"status": "error", "message": "Nodo no encontrado"}), 404
        

        @self.controller.route('/node/<int:node_id>/verify_polynomial/<int:poly_id>')
        def verify_polynomial(node_id, poly_id):
            if node_id < len(self.nodes) and self.nodes[node_id] is not None:
                node = self.nodes[node_id]
                if node.verify_polynomial(poly_id):
                    return jsonify({"status": "success", "message": "Polinomio verificado correctamente"}), 200
                else:
                    return jsonify({"status": "error", "message": "Polinomio incorrecto"}), 400
            return jsonify({"status": "error", "message": "Nodo no encontrado"}), 404


        @self.controller.route('/node/<int:node_id>/verify_dleq/<int:ledger_id>')
        def verify_dleq(node_id, ledger_id):
            failed_nodes = request.args.get('failed_nodes', '').split(',')
            failed_nodes = [int(node) for node in failed_nodes if node]  # Convierte a lista de enteros

            if node_id < len(self.nodes) and self.nodes[node_id] is not None:
                node = self.nodes[node_id]
                if node.verifie_DELQ(ledger_id, failed_nodes):
                    return jsonify({"status": "success", "message": "DLEQ verificado correctamente"}), 200
                else:
                    return jsonify({"status": "error", "message": "DLEQ incorrecto"}), 400
            return jsonify({"status": "error", "message": "Nodo no encontrado"}), 404



        @self.controller.route('/sync_nodes')
        def sync_nodes():
            try:
                self.network.sync_nodes()  # Llama al método de sincronización
                return jsonify({"status": "success", "message": "Sincronización completada"}), 200
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500
        

    def set_nodes(self, nodos):
        self.nodes = nodos  


    def get_blueprint(self):
        return self.controller
