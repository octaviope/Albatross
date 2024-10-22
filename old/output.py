class Output:
 
    def ffte(self, n, L, w, q, p):
        
        if n == 1:
            return L
        
        m = n // 2
        hj = L[:m]
        hjm = L[m:]
        
        u = [0] * m
        v = [0] * m
        
        for j in range(m):
            u[j] = hj[j] * hjm[j]

            invhjm = pow(hjm[j], -1, p)         # Probar con p y q.
            wj = pow(w, j, q)                   # Probar con p y q.
            tmp = ((hj[j] * invhjm) % p)        # Probar con p y q.
            v[j] = pow(tmp, wj, p)              # Probar con p y q.

        w2 = pow(w, 2, q)       # Probar con p y q.

        # Llamadas recursivas
        u2 = self.ffte(m, u, w2, q, p)
        v2 = self.ffte(m, v, w2, q, p)
        
        # Combinación de resultados
        h_hat = u2 + v2

        return h_hat

    


