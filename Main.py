from Funciones import Funciones
from LDEI import LDEI

#Variables

n = 1024 # Numero de participantes
q = 340282366920938463463374607431775848449 # Numero primo
p = 680564733841876926926749214863551696899 # Numero primo
g = [1,2,3,4] # Generadores 
alpha = [1,2,3,4]
k = 4 # Grado del polinomio por defecto 128 creo?
x1 = [1,2,3,4]
P = [1,2,3,4]

'''
f = Funciones()
q, p = f.findprime(0, 0)
print("Numero primo q: ", q)
print("Numero primo p: ", p)
'''

x = LDEI()
z = x.probar(q,p, g, alpha, k, x1, P)
#print("Salida LDEI: ", z)
print(x.verificar(q,p, g, alpha, k, x1))



#x.probar(q,p,g,alpha,k,x1,P)

    #Usamos la funcion print de la clase LEDI
#x.print()

