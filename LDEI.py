import numpy as np #Arrays, vectores y matematicas
from sympy import GF #Matematicas simbolicas
from sympy.polys.domains import ZZ #Dominio de numeros enteros
from sympy.polys.galoistools import gf_random, gf_multi_eval#Para crear un polinomio aleatorio
from sympy.polys.galoistools import * 
import hashlib as hash
from sympy import Mod


class LDEI:
    def __init__(self):
        self._a = np.empty(0) #Vector vacio de enteros mod q. Se llama "a" de array.
        self._e = 0 #Elemento "e" del campo finito mod q
        self._z = np.empty(0) #Vector con los coeficientes del polinomio, estos coeficientes pertenecen al campo finito mod q

    def print(self):
        if(len(self._a)>0):
            print("a: ", self._a, "\ne: ", self._e,"\nz: ", self._z)
        else:
            print("No hay pruebas.")

    # q = Número usado en la operacion mod
    # p = Número usado en la operacion mod
    # g = Vector con los generadores
    # apha = Vector
    # k = grado del polinomio
    # x = Vector
    # P = Polinomio

    #La funcion no devuelve nada sino que modifica los valores e y z. y a[]
    def probar(self, q: int, p: int, g: list[int], alpha: list[int], k: int, x: list[int], P: list[int]):
        #Inicialización con esto hacemos que las operaciones se hagan modulo g
        #¡CUIDADO! Poner los elementos asi "F(3)" para representar que es un elemento del campo finito GF
        GF(q) # Definimos con que modulo se haran las operaciones aunque tengo mi duda de si realmente tiene utilidad porque en todas las funciones me hacen usar el mod q.
        #verify entries
        m = len(g) # Numero de generadores
        #Verificamos que los parametros de entrada sean correctos
        if(len(alpha) != m or len(x) != m or k > m): # El número de componentes alpha, x, o el grado del polinomio es mayor que el número de generadores
            self._a.resize(0) # Reseteamos el vector.
        else: #Creamos el vector a
            R = gf_random(k, q, ZZ) # Creamos un vector R aleatorio de grado k, q es el mod y zz es el dominio de enteros.
            R_eval = gf_multi_eval(R, alpha, q, ZZ) # Devuelve los valores que salen de evaluar R(alpha_i). La solucion.
            GF(p) # Definimos con que modulo se haran las operaciones aunque tengo mi duda de si realmente tiene utilidad porque en todas las funciones me hacen usar el mod q.
            # Crear la estructura de prueba. El modulo pasa a ser p.
            self._a.resize(m) # Reestructuramos el vector para que tenga el tamaño igual al número de generadores
            for i in range(m):
                self._a[i] = pow(g[i], R_eval[i]) #Comprobar si las operaciones se hacen con mod
            
            #Ahora usar mod q

            #hash_ZZp(e, x, a);
            # Convertir los vectores en cadenas de bytes
            cadena_bytes = bytes(str(x) + str(self._a), 'utf-8')

            # Calcular el hash SHA256 de la cadena de bytes
            hash_obj = hash.sha256()
            hash_obj.update(cadena_bytes)
            hash_resultado = hash_obj.hexdigest()
            hash_int = int(hash_resultado, 16)
            self._e = hash_int % q
          

            
            # create z the polynomial of ld
            # ZZ_pX tmp = e * P;
            # z = tmp + R;
            tmp = []
            for i in range(len(P)):
                tmp.append(Mod(self._e * P[i], q)) # No se si val P es un vector y e multiplica a cada coeficiente y luego hay que poner lo coeficientes mod q
            
            for i in range(len(R)):
                self._z = np.append(self._z, Mod(tmp[i] + P[i], q))
                # No se si val P es un vector y tmp suma a cada coeficiente y luego hay que poner lo coeficientes mod q
           
           
            
