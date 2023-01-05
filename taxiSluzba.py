from spade import quit_spade
from time import sleep
import initializer

if __name__ == '__main__':  
    centrala = initializer.Centrala(f"centrala@localhost", f"centrala")
    centrala.start()
    initializer.initTaxi()
    initializer.initPutnici()
    while True:
        try:
            sleep(1)
        except KeyboardInterrupt:
            for t in initializer.Centrala.taxiji:
                t.stop()
            for p in initializer.Centrala.putnici:
                p.stop()
            centrala.stop()
            break
            
    quit_spade()