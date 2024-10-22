import random
import requests

from Proofs.DLEQ import DLEQ
from Network_simulation.ledger import Ledger


class Reveal:
    def __init__(self, ledger: Ledger):
        """Inicializa Reveal con un Ledger."""
        self.ledger: Ledger = ledger  # Accede a los valores desde el ledger

 
    def select_reco_parties(self):
        """Selecciona los nodos reconstructores y genera invsk."""
        leng = self.ledger.n
        self.ledger.r = self.ledger.n - self.ledger.t  # Número mínimo para la reconstrucción
        tab = list(range(leng))  # Lista de participantes

        for i in range(self.ledger.r):  # t + l nodos
            ind = random.randint(0, leng - 1)
            v = tab[ind]
            self.ledger.reco_parties.append(v)  # Elimina el +1, ya que v es el índice correcto
            leng -= 1
            tab[ind:leng] = tab[ind + 1:leng + 1]  # Actualizamos la lista de participantes

        return self.ledger.reco_parties


    def reveal(self):
        """Solicita a los nodos seleccionados que desencripten sus fragmentos localmente y suban el resultado al ledger."""
        self.select_reco_parties()
        # Contactar a cada nodo en reco_parties para que desencripten y suban su fragmento desencriptado
        for i, node_id in enumerate(self.ledger.reco_parties):
            self.request_node_decryption(node_id, i)

        # Sincronizar ledgers.

        # Una vez que todos los fragmentos desencriptados estén en el ledger, puedes continuar con la reconstrucción
        return self.ledger.revealed_fragments, self.ledger.dl

 
    def request_node_decryption(self, node_id, i):
        """Envía una solicitud HTTP al nodo para que desencripte su fragmento localmente y lo suba al ledger."""
        try:
            # Realiza una solicitud HTTP con el parámetro 'i' en la URL
            response = requests.get(f"http://localhost:5000/node/{node_id}/decrypt_fragment", params={'i': i})
            if response.status_code == 200:
                print(f"Nodo {node_id}: fragmento desencriptado y subido con éxito.")
            else:
                print(f"Error al desencriptar el fragmento en el nodo {node_id}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud al nodo {node_id}: {e}")

    

    
