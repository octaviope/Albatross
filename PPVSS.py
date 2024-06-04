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
        self.r = 0 # Número de nodos que quieren reconstrucir el secreto
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

    def setup(self, sk: list, n: int, q: int, p: int, h: int):
        # Creamos las claves secretas
        for i in range(n):
            sk.append(random.randint(1, q - 1))

        # Creamos las claves públicas pk = h^sk
        self.pk = [0] * n
        for i in range(n):
            self.pk[i] = pow(h, sk[i], p)

        # Ponemos los valores en el registro público (self)
        self.n = n
        self.h = h
        self.q = q
        self.p = p
     

    def distribution(self, l: int, t: int, alpha: list):
        # Operaciones mod q
        if(t < 1 or t > self.n):
            return 0
        
        # Elegimos el polinomio P
        deg = t + l
        P = []
        for _ in range(deg+1):
            P.append(random.randint(1, self.q-1))

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

        self.l = l
        self.t = t
        # dist = True
    
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


    def pvss_test(self, n, size):
        # Parametros
        k = 128
        q, p = Funciones.findprime(k, size-k)
      
        t = round(n/3)
        l = n-2*t
        # Operaciones mod p
        gen = Funciones.generator(p)
        h = pow(gen, 2, p)

        # Operaciones mod q
        # Setup
        sk = []

        inicio_tiempo = time.time()
        self.setup(sk, n, q, p, h)
        tiempo_transcurrido = time.time() - inicio_tiempo
        setup_time = tiempo_transcurrido
         

        # Distribucion
        alpha = []
        for i in range(self.n):
            alpha.append((i+1) % q)
        
        inicio_tiempo = time.time()
        self.distribution(l, t, alpha)
        tiempo_transcurrido = time.time() - inicio_tiempo
        dist_time = tiempo_transcurrido

        # Verificacion
        
        if(not self.ld.verificar(q, p, self.pk, alpha, t+l, self.sighat)):
            print("La prueba LDEI no es correcta...")
            return
        
        
        # Comparticion de las partes desencriptadas y prueba DLEQ
        # Selección de nodos reconstructores
        leng = n
        r = n-t
        tab = []
        for i in range(leng):
            tab.append(i)

        invsk = []
        for i in range(r): # t+l nodos
            ind = random.randint(0, leng-1)
            v = tab[ind]
            self.reco_parties.append(v + 1)
            invsk.append(pow(sk[v], -1, q))
            leng -= 1
            for j in range(ind, leng):
                tab[j] = tab[j + 1]

        # Operaciones mod p

        # g y x son matrices de (n-t x 2)
        g = [[] for _ in range(r)]
        x = [[] for _ in range(r)]
        for i in range(r):
            id = self.reco_parties[i]
            x[i].append(h)
            g[i].append(self.sighat[id-1])
            
            inicio_tiempo = time.perf_counter()
            x[i].append(pow(g[i][0], invsk[i], p))
            decrypt_time = time.perf_counter() - inicio_tiempo

            self.sigtilde.append(x[i][1])
            g[i].insert(0, self.pk[id-1])
            
            self.dl.append(DLEQ())
            
            self.dl[i].probar(q,p,g[i],x[i],invsk[i])
        

        for i in range(r):
            if(not (self.dl[i].verificar(q, p, g[i], x[i]))):
                print("Por lo menos una prueba DLEQ es incorrecta...", i)
                
                return
        
        # Reconstrucción
        reco_time = timeit.timeit(lambda: self.reconstruction(r), number=1) 

        # Operaciones mod q
        alphaverif = []
        for j in range(l):
            alphaverif.append(j-l+1)

        for j in range(l, r+l):
            alphaverif.append(self.reco_parties[j-l])

        # Operaciones mod p
        xverif = []
        for j in range(l):
            xverif.append(self.S[j])

        for j in range(l, r+l):
            xverif.append(self.sigtilde[j-l])

        if(not (LDEI.localldei(q,p,alphaverif,t+l,xverif,r+l))):
            print("La reconstrucción no es correcta...")
            return
        
        all_time = setup_time + dist_time + decrypt_time + reco_time

        print("\n\ntimes for q of " ,size , " bits and " , n , " participants in finite field:\n\n")
        print("time for setting up: " , setup_time , "s")
        print("time for distributing: " , dist_time , "s")
        print("time for sharing decrypted shares with dleq: " , decrypt_time , "s")
        print("time for reconstructing the secrets: " , reco_time , "s")

        print("\nglobal time: " , all_time , "s\n\n")
        



        