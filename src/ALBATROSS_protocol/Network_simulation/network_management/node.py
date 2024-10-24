import random
import requests

from ..network_communication.ledger import Ledger
from sympy.polys.galoistools import gf_multi_eval
from sympy.polys.domains import ZZ 
from ...PPVSS.PPVSS import PPVSS
from ...Proofs.DLEQ import DLEQ


class Node:
    def __init__(self, id, node_type, n, q, p, h):
        self.id = id
        self.node_type = node_type  # Tipo de nodo: HONESTO, MALICIOSO, EXTERNO
        self.ledgers: list[Ledger] = [None] * n
        self.ledgers[id] = Ledger(n, q, p, h)
        self.sk = random.randint(0, q - 1)
        self.pk = pow(h, self.sk, p)
        self.neighbors: list[Node] = []   
        self.P = []
        self.S = []
        self.dec_frag = []


    def upload_pk_to_ledger(self):
        """Sube la clave pública al ledger en la posición correspondiente al node_id."""
        for i in range(self.ledgers[self.id].n):
            self.ledgers[i].pk[self.id] = self.pk


    def verifie_LDEI(self, ledger_id):
        ledger: Ledger = self.ledgers[ledger_id]

        if not ledger.ld.verificar(ledger.q, ledger.p, ledger.pk, ledger.alpha, ledger.t + ledger.l, ledger.encrypted_fragments):
            print("La prueba LDEI no es correcta...")
            return False
        return True
    

    def verifie_DELQ(self, decrypt_id, failed_nodes):
        my_ledger: Ledger = self.ledgers[self.id]
        for node_id in failed_nodes:
            failed_ledger: Ledger = self.ledgers[node_id]
        
            g = [my_ledger.pk[decrypt_id], failed_ledger.encrypted_fragments[decrypt_id]]
            x = [my_ledger.h, failed_ledger.revealed_fragments[decrypt_id]]
            if not failed_ledger.dl[decrypt_id].verificar(my_ledger.q, my_ledger.p, g, x):
                print("La prueba DELQ no es correcta...")
                return False
            return True


    def commit(self):
        ledger: Ledger = self.ledgers[self.id]
        ledger.new_ld()
        self.P, self.S, self.dec_frag = PPVSS(ledger).distribute()
        ledger.P = self.P
        self.sync_all_nodes()

        # LDEI
        for node_id in range(ledger.n):
            if node_id != self.id: 
                try:
                    response = requests.get(f"http://localhost:5000/node/{node_id}/verify_lde/{self.id}")
                    if not(response.status_code == 200): 
                        print(f"La verificación LDEI {self.id} en el nodo {node_id} fue incorrecta: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Error en petición de verificación LDEI en el nodo {node_id}: {e}")
        
        return "Commit completado."


    def reveal(self):
        # 1- Subir el polinomio al ledger.
        ledger: Ledger = self.ledgers[self.id]
        # Con nodos maliciosos
        if self.node_type == "MALICIOSO":
            ledger.P = [1]
        else:
            ledger.P = self.P

        self.sync_all_nodes()

        # Verificación del polinomio
        for node_id in range(ledger.n):
            if node_id != self.id: 
                try:
                    response = requests.get(f"http://localhost:5000/node/{node_id}/verify_polynomial/{self.id}")
                    if not(response.status_code == 200): 
                        print(f"La verificación del polinomio subido por el nodo {self.id} fue incorrecta: {response.status_code}")
                        return "verify_polynomial operation failed", 400
                except requests.exceptions.RequestException as e:
                    print(f"Error en la verificación del polinomio en el nodo {node_id}: {e}")

        return "Reveal completado."
    

    def recovery(self, failed_nodes):

        ledger: Ledger = self.ledgers[self.id]

        self.decrypt_fragment(failed_nodes)

        self.sync_all_nodes()

        # Comprobamos que los fragmentos desencriptados son correctos
        for node_id in range(ledger.n):
            try:
                failed_nodes_str = ','.join(map(str, failed_nodes))
                response = requests.get(f"http://localhost:5000/node/{node_id}/verify_dleq/{self.id}?failed_nodes={failed_nodes_str}")

                if not(response.status_code == 200): 
                    print(f"La verificación DLEQ {self.id} en el nodo {node_id} fue incorrecta: {response.status_code}")
                    return "verify_dleq operation failed", 400

            except requests.exceptions.RequestException as e:
                print(f"Error en petición de verificación DLEQ en el nodo {node_id}: {e}")
        

      
        return "Desencriptado correcto"
    

    def output(self):
        lista_int = [int(x) for x in self.S]
        return lista_int
    

    def reconstruction(self, failed_node, reco_parties):
        
        ledger: Ledger = self.ledgers[failed_node]
        for i, e in enumerate(reco_parties):
            reco_parties[i] = e+1

        sec = PPVSS(ledger).reconstruct(reco_parties)
        lista_sec = [int(x) for x in sec]
        return lista_sec
    
    
    def buscar_nodo_por_id(self, id_buscado, visitados=None):
        if visitados is None:
            visitados = set()
        if self.id in visitados:
            return None
        visitados.add(self.id)
        if self.id == id_buscado:
            return self.S, self.dec_frag
        for vecino in self.neighbors:
            resultado = vecino.buscar_nodo_por_id(id_buscado, visitados)
            if resultado:
                return resultado
        return None


    def verify_polynomial(self, poly_id):
        ledger: Ledger = self.ledgers[poly_id]
        # 2- Cada nodo comprueba que el polinomio es correcto.
        evaluations = [gf_multi_eval(ledger.P, [i % ledger.q], ledger.q, ZZ)[0] for i in range(-ledger.l + 1, ledger.n + 1)]
        encrypted_fragments = [pow(ledger.pk[i], evaluations[i + ledger.l], ledger.p) for i in range(ledger.n)]
        for i in range(ledger.n):
            if not (encrypted_fragments[i] == ledger.encrypted_fragments[i]):
                print("El polinomio publicado por el nodo {node_id} no es correcto.")
                return False
        return True

        
    def sync_all_nodes(self):
        try:
            # Realiza una solicitud HTTP para sincronizar todos los nodos
            response = requests.get("http://localhost:5000/sync_nodes")
            if response.status_code != 200:
                print(f"Error en la sincronización: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud de sincronización: {e}")


    def gossip_sync(self):
        """Sincroniza el ledger con los vecinos."""
        for neighbor in self.neighbors:
            self.sync_all_ledgers_with_neighbor(neighbor)


    def sync_all_ledgers_with_neighbor(self, neighbor: "Node"):
        """Sincroniza todos los ledgers con un vecino específico posición por posición.
        Si un ledger está vacío, se copia completo del vecino. Si no, se sincroniza parámetro a parámetro."""
        
        # Iterar sobre todos los ledgers en ambas listas, posición por posición
        for i in range(len(self.ledgers)):
            self_ledger = self.ledgers[i]
            neighbor_ledger = neighbor.ledgers[i]
            
            # Si el vecino no tiene un ledger válido, continuamos con el siguiente
            if neighbor_ledger is None:
                continue
            
            # Si nuestro ledger está vacío (None), copiar el completo del vecino
            if self_ledger is None:
                self.ledgers[i] = neighbor_ledger
            else:
                # Si no está vacío, sincronizamos campo por campo
                self.sync_single_ledger(self_ledger, neighbor_ledger)


    def sync_single_ledger(self, ledger: Ledger, neighbor_ledger: Ledger):
        """Sincroniza los datos de un ledger específico con el ledger del vecino."""
        
        # Sincronizar polinomio
        if ledger.P == [] and neighbor_ledger.P != []:
            ledger.P = neighbor_ledger.P

        # Sincronizar alpha
        if not ledger.alpha and neighbor_ledger.alpha:
            ledger.alpha = neighbor_ledger.alpha

        # Sincronizar r (número de nodos reconstructores)
        if ledger.r == 0 and neighbor_ledger.r > 0:
            ledger.r = neighbor_ledger.r

        # Sincronizar claves públicas (pk)
        for i in range(len(ledger.pk)):
            if ledger.pk[i] == 0 and neighbor_ledger.pk[i] != 0:
                ledger.pk[i] = neighbor_ledger.pk[i]

        # Sincronizar fragmentos cifrados (encrypted_fragments)
        if not ledger.encrypted_fragments and neighbor_ledger.encrypted_fragments:
            ledger.encrypted_fragments = neighbor_ledger.encrypted_fragments

        # Sincronizar fragmentos revelados (revealed_fragments)
        for i in range(len(ledger.revealed_fragments)):
            if ledger.revealed_fragments[i] == 0 and neighbor_ledger.revealed_fragments[i] != 0:
                ledger.revealed_fragments[i] = neighbor_ledger.revealed_fragments[i]

        # Sincronizar nodos reconstructores (reco_parties)
        if not ledger.reco_parties and neighbor_ledger.reco_parties:
            ledger.reco_parties = neighbor_ledger.reco_parties

        # Sincronizar pruebas LDEI (ld)
        if ledger.ld is None and neighbor_ledger.ld is not None:
            ledger.ld = neighbor_ledger.ld

        # Sincronizar pruebas DLEQ (dl)
        for i in range(len(ledger.dl)):
            if ledger.dl[i] == 0 and neighbor_ledger.dl[i] != 0:
                ledger.dl[i] = neighbor_ledger.dl[i]


    def decrypt_fragment(self, failed_nodes):
        my_ledger: Ledger = self.ledgers[self.id]
        invsk = pow(self.sk, -1, my_ledger.q)
        for node_id in failed_nodes:
            other_ledger: Ledger = self.ledgers[node_id]
            encrypted_fragment = other_ledger.encrypted_fragments[self.id]
            decrypted_fragment = pow(encrypted_fragment, invsk, my_ledger.p)
            other_ledger.revealed_fragments[self.id] = decrypted_fragment


            other_ledger.dl[self.id] = DLEQ()
            g = [self.pk, encrypted_fragment]
            x = [my_ledger.h, decrypted_fragment]
            other_ledger.dl[self.id].probar(my_ledger.q, my_ledger.p, g, x, invsk)


    def set_neighbors(self, neighbors):
        self.neighbors = neighbors


    def get_id(self):
        """Devuelve el identificador del nodo."""
        return self.id


    def get_neighbors(self) -> list["Node"]:
        """Devuelve la lista de vecinos del nodo."""
        return self.neighbors

   