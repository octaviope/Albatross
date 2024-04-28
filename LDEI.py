from sympy import GF 
from sympy.polys.domains import ZZ 
from sympy.polys.galoistools import * 
from Hash import Hash
import random


class LDEI:
    def __init__(self):
        self._a = []
        self._e = 0 
        self._z = []

    def print(self):
        if(len(self._a)>0):
            print("a: ", self._a, "\ne: ", self._e,"\nz: ", self._z)
        else:
            print("No hay pruebas.")

    

    def probar(self, q: int, p: int, g: list[int], alpha: list[int], k: int, x: list[int], P: list[int]):
        # Operaciones mod q
        m = len(g) 
        if(len(alpha) != m or len(x) != m or k > m): 
            self._a = self._a[:0]

        else: #Creamos el vector a
            R  = [ random.randint(0, q) for i in range(0, k) ]
            R_eval = gf_multi_eval(R, alpha, q, ZZ) 
            # Operaciones mod p
            for i in range(m):
                self._a.append(pow(g[i], R_eval[i], p))
    
            # Operaciones mod q

            hash = Hash()
            self._e = hash.hash_ZZp(q, x, self._a)

            tmp = gf_mul([self._e], P, q, ZZ)
            self._z = gf_add(tmp, R, q, ZZ)
            
            return self._z
           
    
        

           
            
