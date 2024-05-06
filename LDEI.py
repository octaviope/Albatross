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
            
            
           
    def verificar(self, q: int, p: int, g: list[int], alpha: list[int], k: int, x: list[int]):
        
        m = len(self._a) 

        if(len(alpha) != m or len(x) != m or len(g) != m): 
            print("Verificacion fallida longitud incorrecta.")
            return False
        
        if(gf_degree(self._z) > k):
            print("Verificacion fallida grado de z incorrecto.")
            return False
        
         # Operaciones mod q
        hash = Hash().hash_ZZp(q, x, self._a)
        if (self._e != hash):
            print("Verificacion fallida digest incorrecto.")
            return False
        
        zi = gf_multi_eval(self._z, alpha, q, ZZ)

        # Operaciones mod p
        tmp1, tmp2, tmp3 = 0, 0, 0
        for i in range(m):
            tmp2 = (pow(g[i], int(zi[i]), p))
            tmp3 = (pow(x[i], int(self._e), p))
            tmp1 = gf_mul([tmp3], [self._a[i]], p, ZZ)[0]
            print("tmp1: ", tmp1)###########################################
            print("tmp2: ", tmp2)
            print("tmp3: ", tmp3)
            print("self._a: ", self._a)
            if (tmp2 != tmp1):
                print("Verificacion fallida a_i incorrecto.")
                return False
        return True

    def localldei(q: int, p: int, alpha: list, k: int, x: list ,m: int): #Creo que es un método estático.
        # Operaciones mod q
        u = [0] * m
        for i in range(m):
            prod = 1
            for l in range(m):
                if(l != i):
                    tmp = (alpha[i]-alpha[l]) % q
                    prod = prod * tmp
            u[i] = 1 / prod 

        # Polinomio aleatorio
        P  = [ random.randint(0, q) for i in range(0, m - k - 1) ]
        
        # Calculo de v
        v = [0] * m  
        for i in range(m):
            tmp = gf_multi_eval(P, alpha, q, ZZ) 
            v[i] = (u[i] * tmp) % q

        # Operaciones mod p
        # Verificación
        prod = 1
        for i in range(m):
            tmp = pow(x[i], v[i], p)
            prod = (prod * tmp) % P

        return
        
        
