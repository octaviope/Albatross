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

    

    def probar(self, q: int, p: int, g: int, x: int, alpha: int):
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
            self._e = hash.hash_ZZp(q, x, self._a, g)
      
            tmp = (alpha * self._e) % q 
            self._z = (w - tmp) % q
            if self._z < 0:
                self._z += q

            
            
            
            
           
    def verificar(self, q: int, p: int, g: list[int], x: list[int]):
        # Operaciones mod p
        m = len(self._a)
        if(len(x) != m or len(g) != m): 
            print("Verificacion fallida longitud incorrecta.")
            return False
        
        # Operaciones mod q
        hash = Hash().hash_ZZp(q, x, self._a, g)
        if (self._e != hash):
            print("Verificacion fallida digest incorrecto.")
            return False
        
        # Operaciones mod p
        tmp1, tmp2, tmp3 = 0, 0, 0
        for i in range(m):
            tmp2 = pow(g[i], self._z, p)
            tmp3 = pow(x[i], self._e, p)
            
            tmp1 = (tmp2 * tmp3) % p
            if (self._a[i] != tmp1):
                print("Verificacion fallida a_i incorrecto.",i)
                
#
                return False
        return True   
        

           
            
