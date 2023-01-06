import random
from taxi import Taxi
from putnik import Putnik
from centrala import Centrala
import math

def initTaxi():
    taxiji = []
    for i in range(1, 4):
        taxi = Taxi(f"taxi{i}@localhost", f"taxi{i}")
        taxi.oznaka = f"taxi{i}@localhost"
        taxi.x = random.randrange(1, 60)
        taxi.y = random.randrange(1, 60)
        taxi.redCekanja = []
        taxiji.insert(i, taxi)
        taxi.start()
    
    Centrala.taxiji = taxiji
    
def initPutnici():
    num = random.randrange(3, 10)
    putnici = []
    for i in range(1, num+1):
        putnik = Putnik(f"putnik{i}@localhost", f"putnik{i}")
        putnik.oznaka = f"putnik{i}@localhost"
        putnik.x = random.randrange(1, random.randrange(2, 60))
        putnik.y = random.randrange(1, random.randrange(2, 60))
        putnik.x2 = random.randrange(1, random.randrange(2, 60))
        putnik.y2 = random.randrange(1, random.randrange(2, 60))
        putnik.vrijeme = random.randrange(600, 3600)
        putnik.nasaoTaxi = False
        putnik.odabranTaxi = {}
        putnik.cijena = 0
        putnik.prihvacenaPonuda = False
        putnik.udaljenosti = []
        putnici.insert(i, putnik)
        putnik.start()
    
    Centrala.putnici = putnici
    
def GetUdaljenost(x1, y1, x2, y2):
    return math.sqrt( math.pow( (x2 - x1), 2) + math.pow( (y2 - y1), 2) )

def getCijenu(udaljenost, preostaloVrijeme):
    return udaljenost * (3601 - preostaloVrijeme)