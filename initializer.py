from spade.agent import Agent
import random
from spade.message import Message
from spade.template import Template
from spade import quit_spade

from time import sleep
from taxi import Taxi
from putnik import Putnik
from centrala import Centrala
import math

def initCentrala():
    return Centrala(f"centrala@localhost", f"centrala")

def initTaxi():
    taxiji = []
    for i in range(1, 4):
        taxi = Taxi(f"taxi{i}@localhost", f"taxi{i}")
        taxi.oznaka = f"Taxi-{i}"
        taxi.x = random.randrange(1, 30)
        taxi.y = random.randrange(1, 30)
        taxi.slobodan = True
        taxiji.insert(i, taxi)
        taxi.start()
    
    Centrala.taxiji = taxiji
    
def initPutnici():
    num = random.randrange(1, 30)
    print(num)
    putnici = []
    for i in range(1, 2):
        putnik = Putnik(f"putnik{i}@localhost", f"putnik{i}")
        putnik.oznaka = f"Putnik{i}"
        putnik.x = random.randrange(1, 30)
        putnik.y = random.randrange(1, 30)
        putnik.x2 = random.randrange(1, 30)
        putnik.y2 = random.randrange(1, 30)
        putnik.vrijeme = random.randrange(600, 3600)
        putnik.zatrazioTaxi = False
        putnik.nasaoTaxi = False
        putnici.insert(i, putnik)
        putnik.start()
    
    Centrala.putnici = putnici
    
def GetUdaljenost(x1, y1, x2, y2):
    return math.sqrt( math.pow( (x1 - y1), 2) + math.pow( (x2 - y2), 2) )

def getCijenu(udaljenost, preostaloVrijeme):
    return udaljenost * (3601 - preostaloVrijeme)