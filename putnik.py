import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
import json
import initializer
import asyncio
import datetime

class Putnik(Agent):
    class ZatraziTaxi(PeriodicBehaviour):
        async def run(self):
            if not self.agent.zatrazioTaxi and not self.agent.nasaoTaxi:
                print(f"{self.agent.oznaka} zatrazuje taxi.") 
                await asyncio.sleep(2)                   
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
        async def on_start(self):
            self.odabirem = False
        async def run(self):
            if self.agent.zatrazioTaxi and not self.agent.nasaoTaxi and not self.odabirem == True:
                print(f"{self.agent.oznaka} odabire taxi.")
                self.odabirem = True
                msg = None
                msg = await self.receive(timeout=100)
                if msg:
                    naredba = msg.get_metadata("intent")
                    if naredba == "taxiji":
                        taksisti = json.loads(msg.body)                                                      
                        self.OdaberiTaksista(taksisti)
                        
        def OdaberiTaksista(self, t):
            udaljenosti = []
            for el in t:
                udaljenosti.append(initializer.GetUdaljenost(self.agent.x, self.agent.y, el['x'], el['y']))
            najbliziTaxi = udaljenosti.index(min(udaljenosti))
            print(f"Putnik {self.agent.oznaka} ima sljedece udaljenosti: {udaljenosti}")
            self.agent.odabranTaxi = t[najbliziTaxi]
            self.agent.udaljenosti = udaljenosti            
            self.agent.nudimCijenu = True
            print(f"{self.agent.oznaka} salje zahtjev za prijevoz najblizem taxiju {self.agent.odabranTaxi['oznaka']}.")

            return
                
    class PonudiTaxiju(PeriodicBehaviour):
        async def run(self):
            if (len(self.agent.udaljenosti) == 0): return
            self.agent.vrijeme = self.agent.vrijeme/10
            self.agent.cijena = initializer.getCijenu(min(self.agent.udaljenosti), self.agent.vrijeme)
            if self.agent.nudimCijenu and self.agent.prihvacenaPonuda == False:
                print(f"{self.agent.oznaka} nudi cijenu od {self.agent.cijena} taxiju {self.agent.odabranTaxi}.")
                msg = Message(
                    to=self.agent.odabranTaxi['oznaka'],
                    body=f'{{"cijena":{self.agent.cijena}, "odredisteX":{self.agent.x2}, "odredisteY":{self.agent.y2}}}',
                    metadata={
                        "intent":"ponuda"
                    }
                )
                await self.send(msg)
                
    class VoziSe(CyclicBehaviour):
        async def run(self):
            msg = None
            msg = await self.receive(timeout=11)
            if msg:
                naredba = msg.get_metadata("intent")
                if naredba == "ponuda":
                    if msg.body == "prihvacam":
                        self.agent.prihvacenaPonuda = True
                        print(f"{self.agent.oznaka} i {self.agent.odabranTaxi['oznaka']} se voze na odrediste {self.agent.x2}-{self.agent.y2}")
                        await asyncio.sleep(15)
                        self.agent.x = self.agent.x2
                        self.agent.y = self.agent.y2
                        print(f"{self.agent.oznaka} je stigao na svoje odrediste!")
                        msg = Message(
                            to="centrala@localhost",
                            body=f"{self.agent.oznaka}",
                            metadata={
                                "intent":"putnikRemove"
                            }
                        )
                        await self.send(msg)
                        await self.agent.stop()
                
    
    async def setup(self):
        print(f"Stvoren je putnik {self.oznaka}, na adresi {self.x}-{self.y}, sa ciljem {self.x2}-{self.y2}, i ima {self.vrijeme} vremenskih jedinica da stigne!")
        zatraziPonasanje = self.ZatraziTaxi(period=5)
        odaberiPonasanje = self.OdaberiTaxi()
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
        ponudiPonasanje = self.PonudiTaxiju(period=10, start_at=start_at)
        voziPonasanje = self.VoziSe()
        self.add_behaviour(zatraziPonasanje)
        self.add_behaviour(odaberiPonasanje)
        self.add_behaviour(ponudiPonasanje)
        self.add_behaviour(voziPonasanje)
        
    def encoder_putnik(self):
        return {'oznaka': self.oznaka, 'x': self.x, 'y': self.y, 'x2': self.x2, 'y2': self.y2,
                'vrijeme': self.vrijeme, 'zatrazioTaxi': self.zatrazioTaxi, 'nasaoTaxi': self.nasaoTaxi, 'odabranTaxi': self.odabranTaxi,
                'nudimCijenu': self.nudimCijenu, 'cijena': self.cijena, 'prihvacenaPonuda': self.prihvacenaPonuda, 'udaljenosti': self.udaljenosti}