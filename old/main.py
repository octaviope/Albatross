import sys
import argparse

from protocol.initialization import Initialization
from protocol.distribution import Distribution
from protocol.reveal import Reveal
from protocol.reconstruction import Reconstruction


##################################################################################################
#
##################################################################################################

# Crear el objeto ArgumentParser
parser = argparse.ArgumentParser(description="Procesa dos números de entrada.")
parser.add_argument('--n', type=int, default=512, help='Número de participantes.')
args = parser.parse_args()

if args.n < 100:
    print(f"Error: Número de participantes ({args.n}) es demasiado pequeño se requieren al menos {100}.")
    sys.exit(1)

# Inicialización
init = Initialization()
context = init.setup(args.n, 1024)

# Distribución + verificación LDEI
dist = Distribution(context.n, context.q, context.p, context.pk, context.ld)
context.sighat, context.s, alpha = dist.distribute(context.l, context.t)
if not dist.verificar(context.l, context.t, alpha):
    exit(1)

# Reveal
reveal = Reveal(context.n, context.q, context.p, context.h, context.pk)
context.reco_parties, invsk = reveal.select_reco_parties(context.t, context.sk)
context.sigtilde, context.dl = reveal.reveal(context.sighat, invsk)
if not reveal.verificar_dleq():
    exit(1)

# Reconstrucción
reconstruct = Reconstruction(context.q, context.p, context.l)
context.S = reconstruct.reconstruct(context.sigtilde, context.reco_parties, context.r, context.ld)
if context.S is None:
    print("Error en la reconstrucción.")
    exit(1)

print("Finaliza sin errores.")



##################################################################################################
#
##################################################################################################

