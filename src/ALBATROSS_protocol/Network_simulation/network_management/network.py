import math
import random
import matplotlib.pyplot as plt
import networkx as nx
from .node import Node
from ...PPVSS.Funciones import Funciones

class Network:
    def __init__(self, num_nodes):
        self.nodes: list[Node] = []
        self.n = num_nodes
        self.q = 0
        self.p = 0
        self.h = 0


    def create_nodes(self):
        # Datos de inicialización
        k = 128
        size = 1024
        self.q, self.p = Funciones.findprime(k, size - k)  # q y p generados
        gen = Funciones.generator(self.p)
        self.h = pow(gen, 2, self.p)  # Generador del grupo
    
        for i in range(self.n):
            # Selección de tipo
            r = random.random()
            if r < 0.7:
                node_type = "HONESTO"
            elif r < 0.9:
                node_type = "MALICIOSO"
            else:
                node_type = "EXTERNO"
            
            self.nodes.append(Node(i, node_type, self.n, self.q, self.p, self.h))


    def get_q(self):
        return self.q
    

    def get_p(self):
        return self.p
    

    def get_h(self):
        return self.h


    def pk_to_ledger(self):
        self.sync_nodes()
        for node in self.nodes:
            node.upload_pk_to_ledger()


    def sync_nodes(self, iterations=50):
        """Realiza múltiples rondas de sincronización para propagar las claves públicas."""
        for _ in range(iterations):
            for node in self.nodes:
                node.gossip_sync()


    def assign_neighbors(self):
        max_neighbors = int(math.sqrt(len(self.nodes)))
        for node in self.nodes:
            neighbors = random.sample(self.nodes, k=min(max_neighbors, len(self.nodes) - 1))
            node.set_neighbors([n for n in neighbors if n != node])
            

    def get_nodes(self):
        return self.nodes
    
    
    def get_nodes_by_type(self, node_type):
        return [node for node in self.nodes if node.node_type == node_type]


    def get_node_degree(self, node: Node):
        return len(node.get_neighbors())


    def visualize_network(self):
        G = nx.Graph()

        # Añadir nodos al grafo
        for node in self.nodes:
            G.add_node(node.get_id(), label=node.node_type)

        # Añadir aristas (conexiones entre nodos)
        for node in self.nodes:
            for neighbor in node.get_neighbors():
                G.add_edge(node.get_id, neighbor.get_id)

        # Dibuja la red
        pos = nx.spring_layout(G)  # Disposición para el gráfico
        node_labels = nx.get_node_attributes(G, 'label')

        nx.draw(G, pos, with_labels=False, node_size=500, node_color="skyblue", font_size=10, font_color="black")
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)
        plt.title("Visualización de la red")
        plt.show()
