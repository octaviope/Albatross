# Aqui iran las funciones que seran utilies durante la immplementacion del protocolo Albatross.

from sympy import isprime
from sympy import ZZ, ZZ_p


class Funciones:
    def __init__(self):
        pass 
        
    # k = 128
    # l = n - k = 1024 - 128
    def findprime(self, k: int, l: int):
        n = 2 ** k
        s = (k % 2) - (l % 2)
        tmp = 2 ** l
        q = (tmp + s) * n + 1
        p = 2 * q + 1
        r = 0
        limite = 10 ** 8
        
        while (r < limite): 
            if (isprime(q) and isprime(p)):
                return q, p #Solo puede salir por aqui ya que se pasa como valor
            q += 3 * n
            p += 6 * n
            r += 1 


    def generator(g: int, q: int): #Falta implementar el mod q
        for i in range(2, 2*q + 1):
            po = i**2
            if po == 1:
                continue
            po = i**q
            if po == 1:
                continue
            g = i
            return
        return

        
