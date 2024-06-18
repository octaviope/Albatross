from Funciones import Funciones

class PublicLedger:
    def __init__(self, n, q, p, pk, h):
        self.n = n # Número de nodos
        self.t = round(n/3) # Umbral
        self.l = n-2*self.t # Número de secretos
        self.r = n-self.t # Número de nodos que quieren reconstruir el secreto
        self.q = q
        self.p = p
        self.h = h # Generador del grupo Gq
        self.pk = pk # Claves publicas
        self.sighat = [] # Partes encryptadas
        self.ld = None # Pruebas LDEI
        self.reco_parties = [] # Identificadores de nodos reconstructores
        self.sigtilde = [] # Parets del secreto desencriptadas y su indice
        self.dl = [] # Pruebas DLEQ. Array de objetos DLEQ
        self.S = [] # Secretos reconstruidos

    def get_n(self):
        return self.n
    
    def get_t(self):
        return self.t
    
    def get_l(self):
        return self.l
    
    def get_r(self):
        return self.r
    
    def get_q(self):
        return self.q
    
    def get_p(self):
        return self.p
    
    def get_h(self):
        return self.h
    
    def get_pk(self):
        return self.pk
