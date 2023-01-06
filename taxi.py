from spade.agent import Agent
from spade.message import Message
import asyncio
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
import json
import initializer
import datetime

class Taxi(Agent):
    class PrimajPonude(CyclicBehaviour):
        async def run(self):
            msg = None
            msg = await self.receive(timeout=30)
            if msg:
                naredba = msg.get_metadata("intent")
                if naredba == "ponuda":
                    body = json.loads(msg.body)
                    cijena = body['cijena']
                    odredisteX = body['odredisteX']
                    odredisteY = body['odredisteY']
                    posiljatelj = msg.sender[0] + "@" + msg.sender[1]
                    redCekanja = json.loads(json.dumps(self.agent.redCekanja))
                    if len(redCekanja) == 0:
                        self.agent.redCekanja.append(f'{{"putnik":"{posiljatelj}", "cijena":"{cijena}", "odredisteX":"{odredisteX}", "odredisteY":"{odredisteY}"}}')   
                    else:
                        vecPostoji = False
                        vecaCijena = False
                        putnikZaZamjenu = ""                                            
                        for i in range(0, len(redCekanja)):
                            trenutni = json.loads(redCekanja[i])
                            trenutniPutnik = trenutni['putnik']
                            if posiljatelj == trenutniPutnik:
                                vecPostoji = True
                                if float(cijena) > float(trenutni['cijena']):
                                    vecaCijena = True
                                    putnikZaZamjenu = trenutniPutnik
                        if not vecPostoji:
                            self.agent.redCekanja.append(f'{{"putnik":"{posiljatelj}", "cijena":"{cijena}", "odredisteX":"{odredisteX}", "odredisteY":"{odredisteY}"}}')
                        if vecPostoji and vecaCijena:
                            for i in range(0, len(self.agent.redCekanja)):
                                p = json.loads(redCekanja[i])
                                if putnikZaZamjenu == p['putnik']:
                                    self.agent.redCekanja.pop(i)
                            self.agent.redCekanja.append(f'{{"putnik":"{posiljatelj}", "cijena":"{cijena}", "odredisteX":"{odredisteX}", "odredisteY":"{odredisteY}"}}')
                    msgCentrali = Message(
                        to="centrala@localhost",
                        body=json.dumps(self.agent, default=initializer.Taxi.encoder_taxi, indent=4),
                        metadata={
                            "intent":"taxijiUpdate"
                        }
                    )
                    await self.send(msgCentrali)                                                                                  
            elif not self.agent.vozim:
                msgCentrali = Message(
                    to="centrala@localhost",
                    body=f"{self.agent.oznaka}",
                    metadata={
                        "intent":"taxiRemove"
                    }
                )                
                print(f"{self.agent.oznaka} vise nitko ne treba. Taxi ide na godisnji.")
                await self.send(msgCentrali)
                await self.agent.stop()
        
    class VoziRedCekanja(PeriodicBehaviour):
        async def run(self):
            if len(self.agent.redCekanja) > 0:
                self.agent.redCekanja.sort(key=self.get_cijena, reverse=True)
                prvi = json.loads(self.agent.redCekanja[0])
                msg = Message(
                    to=prvi['putnik'],
                    body="prihvacam",
                    metadata={
                        "intent":"ponuda",
                    }
                )
                await self.send(msg)
                self.agent.vozim = True
                odredisteX = prvi['odredisteX']
                odredisteY = prvi['odredisteY']
                cijena = prvi['cijena']
                self.agent.redCekanja.pop(0)
                print(f"{self.agent.oznaka} vozi {prvi['putnik']} na {odredisteX}-{odredisteY}" + 
                      f" za {cijena} novcanih jedinica.")
                await asyncio.sleep(15)
                self.agent.x = odredisteX
                self.agent.y = odredisteY
                self.agent.vozim = False
                
        def get_cijena(self, element):
            el = json.loads(element)
            return float(el['cijena'])
    
    async def setup(self):
        self.vozim = False
        primajPonasanje = self.PrimajPonude()
        self.add_behaviour(primajPonasanje)
        voziRedCekanjaPonasanje = self.VoziRedCekanja(period=5, start_at=datetime.datetime.now() + datetime.timedelta(seconds=5))
        self.add_behaviour(voziRedCekanjaPonasanje)
        print(f"Pokreće se {self.oznaka}")
        
    def encoder_taxi(self):
        return {'oznaka': self.oznaka, 'x': self.x, 'y': self.y, 'redCekanja': self.redCekanja}