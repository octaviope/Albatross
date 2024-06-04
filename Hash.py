import hashlib

class Hash:
    
    def string_to_int(self, q: int, input: str) -> int:
        output = 0
        for i in input:
            i_elemento = ord(i) % q
            output = (output * 1000 + i_elemento) % q
        return output
    
    def int_to_string(self, x: list[int], a: list[int], g = None) -> str:
        if g is None:
            s = ''.join(str(xi) for xi in x) # convierte cada elemento de x en un string y lo mete en s sin espacios.
            s += ''.join(str(ai) for ai in a)
            return s
        else:
            s = ''.join(str(gi) for gi in g) # convierte cada elemento de x en un string y lo mete en s sin espacios.
            s += ''.join(str(xi) for xi in x)
            s += ''.join(str(ai) for ai in a)
            return s
    
    def sha3_512(self, msg: str) -> str:
        hash_object = hashlib.sha3_512(msg.encode()) # Calcular el hash SHA3-512
        return hash_object.hexdigest() # Devolver el hash en formato hexadecimal
    
    def hash_ZZp (self, q: int, x: list[int], a: list[int], g=None):
        msg = self.int_to_string(x,a,g)
        digest = self.sha3_512(msg)
        return self.string_to_int(q, digest)
        
        



