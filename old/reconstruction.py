from Proofs.LDEI import LDEI
from Network_simulation.ledger import Ledger

class Reconstruction:
    def __init__(self, ledger):
        self.ledger: "Ledger" = ledger  # Asignamos el ledger directamente

    def lambdas(self):
        """Calcula los coeficientes lambda para la reconstrucción."""
        reco_parties = self.ledger.reco_parties
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

                mu = (num * pow(den, -1, q)) % q
                lambs[i][j] = mu
                

        return lambs



    def reconstruct(self):
        """Reconstrucción del secreto utilizando el ledger y verificación local LDEI."""
        
        reco_parties = self.ledger.reco_parties
        sigtilde = self.ledger.revealed_fragments
        r = self.ledger.r
        t = self.ledger.n-self.ledger.t
        l = self.ledger.l
        p = self.ledger.p
        q = self.ledger.q


        if r < t:
            return None, None

        lambs = self.lambdas()

        # Reconstrucción del secreto utilizando los coeficientes lambdas
        Sec = [0] * l  # Ahora guardamos S en el ledger
        for j in range(l):
            Sec[l - j - 1] = 1
            for i in range(t):
                tmp = pow(sigtilde[self.ledger.reco_parties[i]], lambs[i][j], p)
                Sec[l - j - 1] = (Sec[l - j - 1] * tmp) % p

        self.ledger.S = Sec

        # Operaciones mod q y mod p para la verificación LDEI local
        alphaverif = [j - l + 1 for j in range(l)]
        alphaverif += [reco_parties[j - l] for j in range(l, r + l)]
 

        xverif = Sec[:]  # Copia del secreto reconstruido
        xverif += [sigtilde[j - l] for j in range(l, r + l)]


        # Verificación LDEI local
        if not LDEI.localldei(q, p, alphaverif, t + l, xverif, r + l):
            print("La verificación LDEI local falló.")
            return None

        return self.ledger.S
