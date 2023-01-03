import spade
from spade.agent import Agent
import random
from spade.message import Message
from spade.template import Template
from spade import quit_spade
import asyncio
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour

from time import sleep
import json

class Taxi(Agent):
    class PrimajPonude(CyclicBehaviour):
        async def run(self):
            msg = None
            msg = await self.receive(timeout=20)
            if msg:
                naredba = msg.get_metadata("intent")
                if naredba == "ponuda":
                    bodyDict = json.loads(msg.body)
                    cijena = bodyDict['cijena']
                    odredisteX = bodyDict['odredisteX']
                    odredisteY = bodyDict['odredisteY']
                    if self.agent.slobodan == True:
                        self.agent.slobodan = False
                        msg = msg.make_reply()
                        msg.body = "prihvacam"
                        await self.send(msg)
                        print(f"{self.agent.oznaka} vozi putnika na {odredisteX}-{odredisteY} za {cijena} novcanih jedinica.")
                        await asyncio.sleep(15)
                        self.agent.x = odredisteX
                        self.agent.y = odredisteY
                        self.agent.slobodan = True
                    else:
                        self.agent.redCekanja.append(f"{{'putnik':{msg.sender}, 'cijena':{cijena}, 'odredisteX':{odredisteX}, 'odredisteY':{odredisteY}}}")
                        
            elif len(self.agent.redCekanja) > 0 and self.agent.slobodan == True:                  
                self.agent.slobodan = False
                redCekanja = dict(self.agent.redCekanja)
                redCekanja = sorted(redCekanja.items(), key=lambda x:x[1], reverse=True)
                redCekanjaDict = dict(redCekanja)
                print(self.agent.redCekanja)
                print(redCekanja)
                print(redCekanjaDict)
                return
                msg = Message(
                    to=redCekanjaDict[0]['putnik'],
                    body="prihvacam",
                    metadata={
                    "intent":"ponuda"
                    }
                )
                await self.send(msg)
                print(f"{self.agent.oznaka} je opet slobodan i vozi putnika na {redCekanjaDict[0]['odredisteX']}-{redCekanjaDict[0]['odredisteY']} za " +
                    f"{redCekanjaDict[0]['cijena']} novcanih jedinica")
                await asyncio.sleep(15)
                self.agent.x = redCekanjaDict[0]['odredisteX']
                self.agent.y = redCekanjaDict[0]['odredisteY']
                self.agent.slobodan = True
            elif len(self.agent.redCekanja) == 0 and self.agent.slobodan == True:
                print("Vise nema putnika. Taxi ide na godisnji.")
                await self.agent.stop()
    
    
    async def setup(self):
        primajPonasanje = self.PrimajPonude()
        self.add_behaviour(primajPonasanje)
        print(f"Pokreće se {self.oznaka}")
        
    def encoder_taxi(self):
        return {'oznaka': self.oznaka, 'x': self.x, 'y': self.y, 'slobodan': self.slobodan, 'redCekanja': self.redCekanja}