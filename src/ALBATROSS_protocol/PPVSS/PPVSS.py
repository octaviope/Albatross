import random

from sympy.polys.domains import ZZ  
from sympy.polys.galoistools import gf_multi_eval
from ..Proofs.LDEI import LDEI
from ..Network_simulation.network_communication.ledger import Ledger



class PPVSS:
    def __init__(self, ledger: Ledger):
        """Inicializa Reveal con un Ledger."""
        self.ledger: Ledger = ledger  # Accede a los valores desde el ledger


    def distribute(self):

        # Inicialización 
        q = self.ledger.q
        p = self.ledger.p
        n = self.ledger.n
        l = self.ledger.l
        pk = self.ledger.pk

        # Evalucaión del polinomio P
        deg = self.ledger.t + l 
        P = [random.randint(0, q - 1) for _ in range(deg + 1)]
        evaluation = [gf_multi_eval(P, [i % q], q, ZZ)[0] for i in range(-l + 1, n + 1)]
        S = [sec for sec in evaluation[:l]]
        faltantes = [x for x in evaluation if x not in S]

        self.ledger.encrypted_fragments = [pow(pk[i], evaluation[i + l], p) for i in range(n)]

        # LDEI proof
        self.ledger.alpha = [(i + 1) % q for i in range(n)]
        self.ledger.ld.probar(q, p, pk, self.ledger.alpha, deg, self.ledger.encrypted_fragments, P)

        return P, S, faltantes


    
    def lambdas(self, reco_parties):
        """Calcula los coeficientes lambda para la reconstrucción."""
        t = len(reco_parties)
        lambs = [[0] * self.ledger.l for _ in range(t)]
        q = self.ledger.q

        for j in range(self.ledger.l):
            for i in range(t):
                num = 1
                den = 1
                for m in range(t):
                    if m != i:
                        # Calcula y muestra num y den en cada iteración
                        num_step = (-j - reco_parties[m]) % q
                        den_step = (reco_parties[i] - reco_parties[m]) % q
                        
                        # Calcula num y den
                        num = (num * num_step) % q
                        den = (den * den_step) % q
                invden = pow(den, -1, q)
                mu = (num * invden) % q
                lambs[i][j] = mu
                
        return lambs
    

    def reconstruct(self, reco_parties):
        """Reconstrucción del secreto utilizando el ledger y verificación local LDEI."""
        
        sigtilde = [self.ledger.revealed_fragments[party_id - 1] for party_id in reco_parties]

        t = self.ledger.n-self.ledger.t
        r = self.ledger.n - self.ledger.t
        l = self.ledger.l
        p = self.ledger.p
        q = self.ledger.q



        lambs = self.lambdas(reco_parties)
        Sec = [0] * l  # Ahora guardamos S en el ledger
        for j in range(l):
            Sec[l - j - 1] = 1
            for i in range(t):
                tmp = pow(sigtilde[i], lambs[i][j], p)
                Sec[l - j - 1] = (Sec[l - j - 1] * tmp) % p

        print("Reco_parties: ", reco_parties, "\nSecreto reconstruido: ", Sec)

        # Operaciones mod q y mod p para la verificación LDEI local
        alphaverif = [j - l + 1 for j in range(l)]
        alphaverif += [reco_parties[j - l] for j in range(l, r + l)]

 
        xverif = Sec[:]  # Copia del secreto reconstruido
        xverif += [sigtilde[reco_parties[j - l]-1] for j in range(l, r + l)]

        # Verificación LDEI local
        if not LDEI.localldei(q, p, alphaverif, self.ledger.t + l, xverif, r + l):
            print("La verificación LDEI local falló.")
            return False

        return Sec