from ...Proofs.LDEI import LDEI
from ...Proofs.DLEQ import DLEQ


class Ledger:
    def __init__(self, n, q, p, h, pk=None):
        self.n = n
        self.t = round(n // 3) # Umbral de tolerancia
        self.l = n - 2 * self.t # Número de secretos
        self.q = q  # Número primo q
        self.p = p  # Número primo p
        self.h = h  # Generador

        self.pk = pk if pk is not None else [0] * n

        self.P = []
        self.alpha = []
        self.r = 0  # Número de nodos que reconstruyen el secreto
        self.encrypted_fragments = []  # Fragmentos cifrados
        self.revealed_fragments = [0] * n  # Fragmentos revelados
        self.reco_parties = []  # Nodos reconstructores
        self.ld = None  # Pruebas LDEI
        self.dl: list[DLEQ] = [0] * (self.n) # Pruebas DLEQ. Array de objetos DLEQ


    def new_ld(self):
        self.ld = LDEI()
    

    def get_r(self):
        return self.r


    def show_ledger(self):
        """Muestra el estado actual del ledger."""
        print("---- Ledger ----")
        print(f"Número de participantes (n): {self.n}")
        print(f"Primo q: {self.q}")
        print(f"Primo p: {self.p}")
        print(f"Generador h: {self.h}")
        print(f"Umbral de tolerancia (t): {self.t}")
        print(f"Número de secretos (l): {self.l}")
        print(f"Número de nodos reconstructores (r): {self.r}")
        
        print("\nClaves públicas (pk):")
        for i, pk_value in enumerate(self.pk):
            print(f"  Nodo {i}: {pk_value}")

        print("\nFragmentos cifrados (encrypted_fragments):")
        for i, frag in enumerate(self.encrypted_fragments):
            print(f"  Nodo {i}: {frag}")

        print("\nFragmentos revelados (revealed_fragments):")
        for i, revealed in enumerate(self.revealed_fragments):
            print(f"  Nodo {i}: {revealed}")

        print("\nNodos reconstructores (reco_parties):")
        print(self.reco_parties)

        print("\nPruebas LDEI:")
        if self.ld:
            print(f"LDEI Prueba: {self.ld}")
        else:
            print("LDEI no inicializado")

        print("\nPruebas DLEQ:")
        for i, dleq in enumerate(self.dl):
            print(f"  Nodo {i}: {dleq}")
        print("----------------")
