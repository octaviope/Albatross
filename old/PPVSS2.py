from initialization import Initialization
from distribution import Distribution
from reveal import Reveal
from reconstruction import Reconstruction

def pvss_test(n, ledger):
    # Inicialización
    init = Initialization()
    context = init.setup(n, 1024)

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