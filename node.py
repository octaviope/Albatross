import requests
from ledger import PublicLedger
from threading import Thread
from Protocol import PPVSS

class Node:
    def __init__(self, id, sk, pk, n, q, p, h):
        self.id = id
        self.sk = sk
        self.pk = pk 
        self.n = n 
        self.q = q 
        self.p = p 
        self.h = h
        self.ledger = []

    def execute_protocol(self):
        self.ledger.append(PublicLedger( self.n, self.q, self.p, self.pk, self.h))
        ledger_id = len(self.ledger)-1
        PPVSS().pvss_test(self.ledger[ledger_id])


        return {"status": "success", "message": "Protocolo ejecutado"}


    def get_invsk(self):
        return pow(self.sk, -1, self.q)
