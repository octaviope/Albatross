from .verification.LDEI import LDEI

class ProtocolContext:
    def __init__(self, n, q, p, h, l, t, sk, pk):
        self.n = n  # Número de participantes
        self.q = q  # Número primo q
        self.p = p  # Número primo p
        self.h = h  # Generador
        self.r = 0  # Número de nodos que quieren reconstruir el secreto
        self.l = l  # Número de secretos
        self.t = t  # Umbral de tolerancia
        self.sk = sk  # Claves privadas
        self.pk = pk  # Claves públicas
        self.sighat = []  # Fragmentos cifrados
        self.sigtilde = []  # Fragmentos revelados
        self.reco_parties = []  # Nodos reconstructores
        self.s = []  # Secretos
        self.S = []  # Secretos reconstruidos
        self.ld = LDEI() # Pruebas LDEI
        self.dl = [] # Pruebas DLEQ. Array de objetos DLEQ
