import unittest
from Hash import Hash
from LDEI import LDEI

class Tests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hash variables
        self.h = Hash()
        self.LDEI = LDEI()
        self.lista1 = [1, 2, 3, 4, 5]
        self.lista2 = [7, 4, 9, 2, 6]
        
    ### LDEI Tests ###
    def test_probar(self):
        #resultado = self.LDEI.probar(q, p, g, alpha, k, x, P)
        self.assertEqual("resultado", "1234574926", "Resultado esperado: .")

    
    ### Hash Tests ###
    def test_1_int_to_string(self):
        resultado = self.h.int_to_string(self.lista1, self.lista2)
        self.assertEqual(resultado, "1234574926", "Resultado esperado: \"1234574926\".")

    def test_2_sha3_512(self):
        resultado = self.h.sha3_512("1234574926")
        self.assertEqual(resultado, "0933f65a52e405c952364e14ed844aed5684b1cfe0bf17946518eff07ebfb6cda4ee3998b6286cb76662f98190549f48f94a3d0d52d65fac5ca06d21dc344358", 
                         "Resultado esperado: \"0933f65a52e405c952364e14ed844aed5684b1cfe0bf17946518eff07ebfb6cda4ee3998b6286cb76662f98190549f48f94a3d0d52d65fac5ca06d21dc344358\".")

    def test_3_string_to_int(self):
        resultado = self.h.string_to_int(7, "0933f65a52e405c952364e14ed844aed5684b1cfe0bf17946518eff07ebfb6cda4ee3998b6286cb76662f98190549f48f94a3d0d52d65fac5ca06d21dc344358")
        self.assertEqual(int(resultado), 1, "Resultado esperado: 0.")

    def test_4_hash_ZZp(self):
        resultado = self.h.hash_ZZp(7, self.lista1, self.lista2)
        self.assertEqual(int(resultado), 1, "Resultado esperado: 0.")


if __name__ == '__main__':
    unittest.main()

