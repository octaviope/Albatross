import requests
from Funciones import Funciones
from sympy.polys.domains import ZZ 
from sympy.polys.galoistools import * 
from LDEI import LDEI
from DLEQ import DLEQ
import random
import timeit
import time

class PPVSS:
    def __init__(self):
        self.n = 0 # Número de nodos
        self.t = 0 # Umbral
        self.l = 0 # Número de secretos
        self.r = 0 # Número de nodos que quieren reconstruir el secreto
        self.q = 0 # Orden del grupo Gq
        self.p = 0 # 2q + 1
        self.h = 0 # Generador del grupo Gq
        self.pk = [] # Claves publicas
        self.sighat = [] # Partes encryptadas
        self.ld = LDEI() # Pruebas LDEI
        self.reco_parties = [] # Identificadores de nodos reconstructores
        self.sigtilde = [] # Parets del secreto desencriptadas y su indice
        self.dl = [] # Pruebas DLEQ. Array de objetos DLEQ
        self.S = [] # Secretos reconstruidos

   
     

    def distribution(self, l: int, t: int, alpha: list):
        # Operaciones mod q
        if(t < 1 or t > self.n):
            return 0
        
        # Elegimos el polinomio P
        deg = t + l
        P = []
        for _ in range(deg):
            P.append(random.randint(0, self.q-1))

        # Cálculo de las partes de shamir
        s = []
        for i in range(-l+1, self.n+1):
            s.append(gf_multi_eval(P, [i % self.q], self.q, ZZ)[0])

        # Operaciones mod p
        # Proceso para calcular partes encriptadas
        self.sighat = [] 
        for i  in range(self.n):
            self.sighat.append(pow(self.pk[i], s[i+l], self.p))
        
        # Proceso para calcular la prueba LDEI
        self.ld.probar(self.q, self.p, self.pk, alpha, deg, self.sighat, P)



    def lambdas(self, lambs: list, t: int):
        # Operaciones mod q
        
        for j in range(self.l):
            for i in range(t):
                num = 1
                den = 1
                for m in range(t):
                    if(m != i):
                        tmp = (-j - self.reco_parties[m]) % self.q
                        num = (num*tmp) % self.q
                        tmp = (self.reco_parties[i] - self.reco_parties[m]) % self.q
                        den = (den * tmp) % self.q
                invden =  pow(den, -1, self.q)
                mu = (num * invden) % self.q
                lambs[i][j] = mu


    def reconstruction(self, r: int):
        t = self.n - self.t
        if r < t:
            return
        # Operaciones mod q
        lambs = [[0] * self.l for _ in range(t)]

        self.lambdas(lambs, t)

        # Operaciones mod p
        self.S = [0] * self.l
        for j in range(self.l):
            self.S[self.l-j-1] = 1
            for i in range(t):
                
                tmp = pow(self.sigtilde[i], lambs[i][j], self.p)
                self.S[self.l-j-1] = (self.S[self.l-j-1] * tmp) % self.p

        self.r = r
        return
    
    def setup_ledger(self, ledger):
        self.n = ledger.get_n() 
        self.t = ledger.get_t()
        self.l = ledger.get_l()
        self.r = ledger.get_r()
        self.q = ledger.get_q()
        self.p = ledger.get_p()
        self.h = ledger.get_h()
        self.pk = ledger.get_pk()
        return
    
    def get_invsk(self, other_node_url):
        # Método para solicitar invsk 'http://localhost:5000/node/<int:node_id>/get_id'
        response = requests.get(other_node_url + '/get_invsk')
        if response.status_code == 200:
            return response.json()['invsk']
        else:
            return None
        

    def pvss_test(self, ledger):
        #Setup
        self.setup_ledger(ledger)

        # Distribucion
        alpha = []
        for i in range(self.n):
            alpha.append((i+1) % self.q)
        self.distribution(self.l, self.t, alpha)

        # Verificacion
        if(not self.ld.verificar(self.q, self.p, self.pk, alpha, self.t+self.l, self.sighat)):
            print("La prueba LDEI no es correcta...")
            return
        
        
        # Comparticion de las partes desencriptadas y prueba DLEQ
        # Selección de nodos reconstructores
        leng = self.n
        r = self.n-self.t
        tab = []
        for i in range(leng):
            tab.append(i)

        invsk = []
        for i in range(r): # t+l nodos
            ind = random.randint(0, leng-1)
            v = tab[ind]
            self.reco_parties.append(v + 1)
            ############################################
            invsk.append(self.get_invsk(f'http://localhost:5000/node/{v}'))
            ############################################
            leng -= 1
            for j in range(ind, leng):
                tab[j] = tab[j + 1]

        # Operaciones mod p

        # g y x son matrices de (n-t x 2)
        g = [[] for _ in range(r)]
        x = [[] for _ in range(r)]
        for i in range(r):
            id = self.reco_parties[i]
            x[i].append(self.h)
            g[i].append(self.sighat[id-1])
            
            inicio_tiempo = time.perf_counter()
            x[i].append(pow(g[i][0], invsk[i], self.p))
            decrypt_time = time.perf_counter() - inicio_tiempo

            self.sigtilde.append(x[i][1])
            g[i].insert(0, self.pk[id-1])
            
            self.dl.append(DLEQ())
            
            self.dl[i].probar(self.q,self.p,g[i],x[i],invsk[i])
        

        for i in range(r):
            if(not (self.dl[i].verificar(self.q, self.p, g[i], x[i]))):
                print("Por lo menos una prueba DLEQ es incorrecta...", i)
                
                return
        
        # Reconstrucción
        self.reconstruction(r)
        # Operaciones mod q
        alphaverif = []
        for j in range(self.l):
            alphaverif.append(j-self.l+1)

        for j in range(self.l, r+self.l):
            alphaverif.append(self.reco_parties[j-self.l])

        # Operaciones mod p
        xverif = []
        for j in range(self.l):
            xverif.append(self.S[j])

        for j in range(self.l, r+self.l):
            xverif.append(self.sigtilde[j-self.l])

        if(not (LDEI.localldei(self.q,self.p,alphaverif,self.t+self.l,xverif,r+self.l))):
            print("La reconstrucción no es correcta...")
            return
        
        return "Sol: ", self.S
        



        