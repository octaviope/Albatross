from sympy import isprime
class Funciones:
    @staticmethod
    def findprime(k: int, l: int):
        n = 2 ** k
        s = (k % 2) - (l % 2)
        tmp = 2 ** l
        q = (tmp + s) * n + 1
        p = 2 * q + 1
        limite = 10 ** 8
        
        for _ in range(limite):
            if (isprime(q) and isprime(p)):
                return q, p
            q += 3 * n
            p += 6 * n

        print("Números primos no encontrados.")
        return None, None

    @staticmethod
    def generator(q:int): 
        for i in range(2, 2*q + 1):
            po = pow(i, 2, q)
            if po == 1:
                continue
            po = pow(i, q, q)
            if po == 1:
                continue
            return i 
        return

    @staticmethod
    def rootunity(n, q):
        i = 2  
        t = (q - 1) / n 
        while True:
            w = pow(int(i), int(t), int(q))
            tmp = pow(int(w), int(n / 2), int(q))
            if tmp != 1:
                return w
            i += 1

        