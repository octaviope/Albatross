from sympy import GF 
from sympy.polys.domains import ZZ 
from sympy.polys.galoistools import * 
from Hash import Hash
import random


class DLEQ:
    def __init__(self):
        self._a = []
        self._e = 0 
        self._z = 0

    def print(self):
        if(len(self._a)>0):
            print("a: ", self._a, "\ne: ", self._e,"\nz: ", self._z)
        else:
            print("No hay pruebas.")

    

    def probar(self, q: int, p: int, g: list[int], x: list[int], alpha: list[int]):
        # Operaciones mod p
        m = len(g) 
        if(len(x) != m): 
            self._a = self._a[:0]

        else: 
            # Operaciones mod q
            w = random.randint(0, q-1)

            # Operaciones mod p
            for i in range(m):
                self._a.append(pow(g[i], w, p))
    
            # Operaciones mod q
            hash = Hash()
            self._e = hash.hash_ZZp(q, g, x, self._a)

            tmp = gf_mul(alpha, self._e, q, ZZ)
            self._z = gf_sub(w, tmp, q, ZZ)
            
            
           
    def verificar(self, q: int, p: int, g: list[int], x: list[int]):
        # Operaciones mod p
        m = len(self._a) 
        if(len(x) != m or len(g) != m): 
            print("Verificacion fallida longitud incorrecta.")
            return False
        
        # Operaciones mod q
        hash = Hash().hash_ZZp(q, g, x, self._a)
        if (self._e != hash):
            print("Verificacion fallida digest incorrecto.")
            return False
        
        # Operaciones mod p
        tmp1, tmp2, tmp3 = 0, 0, 0
        for i in range(m):
            tmp2 = (pow(g[i], int(self._z), p))
            tmp3 = (pow(x[i], int(self._e), p))
            tmp1 = gf_mul([tmp2], [tmp3], p, ZZ)[0]
            print("tmp1: ", tmp1)
            print("tmp2: ", tmp2)
            print("tmp3: ", tmp3)
            print("self._a: ", self._a)
            if (self._a[i] != tmp1):
                print("Verificacion fallida a_i incorrecto.")
                return False
        return True   
        

           
            
