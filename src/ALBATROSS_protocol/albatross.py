import random
import threading
import requests

from .PPVSS.Funciones import Funciones


class Albatross:
    def __init__(self, network, num_participants):
        self.network = network
        self.num_participants = num_participants
        self.t = round(num_participants / 3)
        self.successful_commit_ids = set()
        self.successful_reveal_ids = set()
        self.successful_recovery_ids = set()
        self.successful_decrypt_ids = set()
        self.T = []
        self.col_R = []


    def request_commit(self, node_id):
        try:
            response = requests.get(f"http://localhost:5000/node/{node_id}/commit")
            if (response.status_code == 200) and (len(self.successful_commit_ids) < (self.num_participants - self.t)):  # Verifica si el commit fue exitoso
                self.successful_commit_ids.add(node_id)  # Agrega el node_id si fue exitoso
                print(f"Commit exitoso en nodo {node_id}: {response.text}")
            else:
                print(f"Fallo en el commit del nodo {node_id}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error ejecutando el commit en nodo {node_id}: {e}")


    def request_reveal(self, node_id):
        try:
            response = requests.get(f"http://localhost:5000/node/{node_id}/reveal")
            if response.status_code == 200:  # Verifica si el reveal fue exitoso
                self.successful_reveal_ids.add(node_id)  # Agrega el node_id si el reveal fue exitoso
                print(f"Reveal exitoso en nodo {node_id}: {response}")
            else:
                print(f"Fallo en el reveal del nodo {node_id}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error ejecutando el reveal en nodo {node_id}: {e}")


    def request_output(self, node_id):
        try:
            response = requests.get(f"http://localhost:5000/node/{node_id}/output")
            if response.status_code == 200:  # Verifica si el reveal fue exitoso
                # Accede al contenido de la respuesta como JSON
                json_response = response.json()
                decoded_response = json_response.get('result', [])

                # Convierte los elementos de la lista a enteros, si es necesario
                numbers = [int(x) for x in decoded_response]
                
                self.T.append(numbers)
                print(f"Extracción de aleatoriedad exitosa en nodo {node_id}")
            else:
                print(f"Fallo en el output del nodo {node_id}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error ejecutando el output en nodo {node_id}: {e}")


    def request_recovery(self, node_id, failed_nodes):
        try:
            # Convierte los failed_nodes en un string separado por comas
            failed_nodes_str = ','.join(map(str, failed_nodes))
            response = requests.get(f"http://localhost:5000/node/{node_id}/recovery?failed_nodes={failed_nodes_str}")
            
            if response.status_code == 200:
                self.successful_recovery_ids.add(node_id)
                print(f"Recovery exitoso en nodo {node_id}")
            else:
                print(f"Fallo en el recovery del nodo {node_id}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error ejecutando el reveal en nodo {node_id}: {e}")
    
    
    def request_reconstruction(self, reco_id, node_id, reco_parties):
        try:
            reco_part = ','.join(map(str, reco_parties))
            response = requests.get(f"http://localhost:5000/node/{reco_id}/reconstruction/{node_id}?reco_parties={reco_part}")

            
            if response.status_code == 200:
                # Accede al contenido de la respuesta como JSON
                json_response = response.json()
                decoded_response = json_response.get('result', [])

                # Convierte los elementos de la lista a enteros, si es necesario
                numbers = [int(x) for x in decoded_response]

                
                self.T.append(numbers)
                print(f"Reconstrucción exitosa del nodo {node_id}")
            else:
                print(f"Fallo en la reconstrucción del nodo {node_id}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error ejecutando la reconstrucción en el nodo {node_id}: {e}")



           

    def execute_commit_phase(self):
        threads = []
        print("Ejecutando las peticiones de commit...")
        for i in range(self.num_participants):
            thread = threading.Thread(target=self.request_commit, args=(i,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()


    def execute_reveal_phase(self):
        threads = []
        print("Ejecutando las peticiones de reveal...")
        for node_id in self.successful_commit_ids:
            thread = threading.Thread(target=self.request_reveal, args=(node_id,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()


    def handle_output_phase(self):
        if len(self.successful_reveal_ids) == (self.num_participants - self.t):
            print("Todas las revelaciones fueron exitosas.")
            self.process_output()
        else:
            print("Alguna revelación falló. Procediendo con la acción alternativa.")
            self.execute_recovery_phase()


    def ffte(self, n, L, w, q, p):
        
        if n == 1:
            return L
        
        m = n // 2
        hj = L[:m]
        hjm = L[m:]
        
        u = [0] * m
        v = [0] * m
        
        for j in range(m):
            u[j] = hj[j] * hjm[j]

            invhjm = pow(hjm[j], -1, p)         # Probar con p y q.
            wj = pow(w, j, q)                   # Probar con p y q.
            tmp = ((hj[j] * invhjm) % p)        # Probar con p y q.
            v[j] = pow(tmp, wj, p)              # Probar con p y q.

        w2 = pow(w, 2, q)       # Probar con p y q.

        # Llamadas recursivas
        u2 = self.ffte(m, u, w2, q, p)
        v2 = self.ffte(m, v, w2, q, p)
        
        # Combinación de resultados
        h_hat = u2 + v2

        return h_hat


    def process_output(self):
        threads = []
        for node_id in self.successful_reveal_ids:
            thread = threading.Thread(target=self.request_output, args=(node_id,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        self.process_final_output()


    def process_final_output(self):
        print("Número de iteraciones(filas): ", len(self.T))
        w = Funciones.rootunity(len(self.T[0]), self.network.get_q()) 
        self.T = list(map(list, zip(*self.T)))  
        for i in range(len(self.T)):
            for j, sec in enumerate(self.T[i]):
                self.T[i][j] = pow(self.network.get_h(), sec, self.network.get_q())
            self.col_R.append(self.ffte(len(self.T[i]), self.T[i], w, self.network.get_q(), self.network.get_p())) 
        R = list(map(list, zip(*self.col_R))) 
        exit(0)


    def execute_recovery_phase(self):
        threads = []
        failed_nodes = self.successful_commit_ids - self.successful_reveal_ids 

        for node_id in range(self.num_participants):
            thread = threading.Thread(target=self.request_recovery, args=(node_id, failed_nodes))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()

        if len(self.successful_recovery_ids) >= (self.num_participants - self.t):
            print("Se procede con la reconstrucción de secretos.")
            self.execute_reconstruction_phase(failed_nodes)
        else:
            print("No se puede reconstruir el secreto, el número de participantes bien intencionados es insuficiente.")
            exit(-1)


    def execute_reconstruction_phase(self, failed_nodes):

        threads = []
        for node_id in self.successful_reveal_ids:
            thread = threading.Thread(target=self.request_output, args=(node_id,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

        # convierto la matriz a elementos h^s
        for lista in self.T: 
            for i in range(len(lista)):
                lista[i] = pow(self.network.h, lista[i], self.network.p)
            
        
        threads = []
        participantes = list(range(self.num_participants))
        for node_id in failed_nodes: 
            # Quitamos el nodo a reconstruir
            if node_id in participantes:
                participantes.remove(node_id)

            # Elegimos reco_parties
            tam_subgrupo = self.num_participants * 2 // 3
            subgrupo = random.sample(participantes, tam_subgrupo)

            
            thread = threading.Thread(target=self.request_reconstruction, args=(node_id, subgrupo[0], subgrupo))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()

        ####################################
        ##### Cálculo final del output #####
        ####################################
        # Crear matriz M con w.
        # Sacar output multiplicando M * T en el exponente.
        
        print("Reconstrucción de secretos completada.")



