# Aqui iran las funciones que seran utilies durante la immplementacion del protocolo Albatross.
import gmpy2

class Funciones:

    def findprime(k: int, l: int):
        if(l+k == 1024): 
            return 179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586385388643390959266778519315941857485555499009, 359538626972463181545861038157804946723595395788461314546860162315465351611001926265416954644815072042240227759742786715317579537628833244985694861278948248755535786849730970552604439202492188238906165904170011537676301364684925762947826221081654474326701021369172770777286781918533557038631883714971110998019
        else:
            n = 2 ** k
            s = (k % 2) - (l % 2)
            tmp = 2 ** l
            q = (tmp + s) * n + 1
            p = 2 * q + 1
            limite = 10 ** 8
            
            for _ in range(limite):
                if (gmpy2.is_prime(q) and gmpy2.is_prime(p)):
                    return q, p
                q += 3 * n
                p += 6 * n

            print("Números primos no encontrados.")
            return None, None


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

        