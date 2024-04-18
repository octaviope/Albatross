import unittest

class TestCalculadora(unittest.TestCase):

    # Prueba para la función sumar
    def test_sumar(self):
        resultado = self.calc.sumar(2, 3)
        self.assertEqual(resultado, 5, "La suma de 2 y 3 debería ser 5")

    

