import hashlib
from sympy import GF

class Hash:
    
    def string_to_int(self, q: int, input: str) -> int:
        GF_q = GF(q)
        output = GF_q(0) # Inicializamos el resultado como un elemento del anillo de Galois
        # Iterar sobre cada carácter de la cadena de entrada
        for i in input:
            # Convertir el carácter en un elemento del anillo de Galois
            i_elemento = GF_q(ord(i))
            # Realizar la multiplicación y suma modular
            output = (output * 1000) + i_elemento
        return output

    def int_to_string(self, x: list[int], a: list[int]) -> str:
        s = ''.join(str(xi) for xi in x) # convierte cada elemento de x en un string y lo mete en s sin espacios.
        s += ''.join(str(ai) for ai in a)
        return s
    
    def sha3_512(self, msg: str) -> str:
        hash_object = hashlib.sha3_512(msg.encode()) # Calcular el hash SHA3-512
        return hash_object.hexdigest() # Devolver el hash en formato hexadecimal
    
    def hash_ZZp (self, q: int, x: list[int], a: list[int]):
        msg = self.int_to_string(x,a)
        digest = self.sha3_512(msg)
        print("Mensaje: ", msg)
        print("Codigo hash: ", digest)
        return self.string_to_int(q, digest)
        
        



