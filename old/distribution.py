import random
from sympy.polys.domains import ZZ  
from sympy.polys.galoistools import gf_multi_eval
from Network_simulation.ledger import Ledger

class Distribution:
    def __init__(self, ledger):
        self.ledger: Ledger = ledger  

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
        self.ledger.encrypted_fragments = [pow(pk[i], evaluation[i + l], p) for i in range(n)]

        # LDEI proof
        self.ledger.alpha = [(i + 1) % q for i in range(n)]
        self.ledger.ld.probar(q, p, pk, self.ledger.alpha, deg, self.ledger.encrypted_fragments, P)

        return P, S
