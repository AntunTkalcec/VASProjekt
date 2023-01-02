import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
import json
import initializer
import asyncio

class Putnik(Agent):
    class ZatraziTaxi(PeriodicBehaviour):
        async def run(self):
            if not self.agent.zatrazioTaxi and not self.agent.nasaoTaxi:
                print(f"{self.agent.oznaka} zatrazuje taxi.")
                msg = Message(
                    to="centrala@localhost",
                    body="",
                    metadata={
                        "intent":"taxiji",
                    }
                )
                await self.send(msg)
                self.agent.zatrazioTaxi = True
                
    class OdaberiTaxi(CyclicBehaviour):
        async def run(self):
            if self.agent.zatrazioTaxi and not self.agent.nasaoTaxi:
                print(f"{self.agent.oznaka} odabire taxi.")
                msg = None
                msg = await self.receive(timeout=100)
                if msg:
                    naredba = msg.get_metadata("intent")
                    if naredba == "taxiji":
                        taksisti = json.loads(msg.body)                               
                        for el in taksisti:
                            print(el)
                        self.OdaberiTaksista(taksisti)
                        
        def OdaberiTaksista(self, t):
            if len(t) == 0:
                print("Nema slobodnih taksista")
                return
            udaljenosti = []
            for el in t:
                udaljenosti.append(initializer.GetUdaljenost(self.agent.x, self.agent.y, el['x'], el['y']))
            najbliziTaxi = udaljenosti.index(min(udaljenosti))
            self.agent.nasaoTaxi = True
            print(f"{self.agent.oznaka} je od {t[0]['oznaka']} udaljen {initializer.GetUdaljenost(self.agent.x, self.agent.y, t[0]['x'], t[0]['y'])} jedinica.")
                
    
    async def setup(self):
        print(f"Stvoren je putnik {self.oznaka}, na adresi {self.x}-{self.y}, sa ciljem {self.x2}-{self.y2}, i ima {self.vrijeme} vremenskih jedinica da stigne!")
        zatraziPonasanje = self.ZatraziTaxi(period=5)
        odaberiPonasanje = self.OdaberiTaxi()
        self.add_behaviour(zatraziPonasanje)
        self.add_behaviour(odaberiPonasanje)
        
    def encoder_putnik(self):
        return {'oznaka': self.oznaka, 'x': self.x, 'y': self.y, 'x2': self.x2, 'y2': self.y2,
                'vrijeme': self.vrijeme, 'zatrazioTaxi': self.zatrazioTaxi, 'nasaoTaxi': self.nasaoTaxi}