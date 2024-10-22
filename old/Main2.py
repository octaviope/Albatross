import sys
from Funciones import Funciones
from verification.LDEI import LDEI
from PPVSS import PPVSS
import argparse


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


# Ejecución
ppvss = PPVSS()
ppvss.pvss_test(args.n, 1024)


##################################################################################################
#
##################################################################################################

