from spade.agent import Agent
from spade.message import Message
from spade.template import Template
from spade import quit_spade

from time import sleep
from centrala import Centrala
import initializer

if __name__ == '__main__':  
    centrala = Centrala(f"centrala@localhost", f"centrala")
    centrala.start()
    initializer.initTaxi()
    initializer.initPutnici()
    while True:
        try:
            sleep(1)
        except KeyboardInterrupt:
            for t in Centrala.taxiji:
                t.stop()
            for p in Centrala.putnici:
                p.stop()
            centrala.stop()
            break
            
    quit_spade()