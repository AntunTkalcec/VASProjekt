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
import initializer
import datetime

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
                    if self.agent.slobodan == True and len(self.agent.redCekanja) == 0:
                        self.agent.slobodan = False
                        msg = msg.make_reply()
                        msg.body = "prihvacam"
                        await self.send(msg)
                        print(f"{self.agent.oznaka} vozi putnika na {odredisteX}-{odredisteY} za {cijena} novcanih jedinica.")
                        await asyncio.sleep(15)
                        self.agent.x = odredisteX
                        self.agent.y = odredisteY
                    elif self.agent.slobodan == False:
                        self.agent.redCekanja.append(f"{{'putnik':{msg.sender}, 'cijena':{cijena}, 'odredisteX':{odredisteX}, 'odredisteY':{odredisteY}}}")
                        msgCentrali = Message(
                            to="centrala@localhost",
                            body=json.dumps(self.agent, default=initializer.Taxi.encoder_taxi, indent=4),
                            metadata={
                                "intent":"taxijiUpdate"
                            }
                        )
                        await self.send(msgCentrali) 
                                           
            else:
                print(f"{self.agent.oznaka} vise nitko ne treba. Taxi ide na godisnji.")
                await self.agent.stop()

        def get_cijena(element):
            return element['cijena']
        
    class VoziRedCekanja(PeriodicBehaviour):
        async def run(self):
            if len(self.agent.redCekanja) > 0 and self.agent.slobodan == True:
                self.agent.slobodan = False
                test = self.agent.redCekanja
                testSorted = sorted(test, reverse=True, key=lambda element: element[1])
                return
                test2 = test.items()
                redCekanja = sorted(redCekanja.items(), key=lambda x:x[1], reverse=True)
                redCekanjaDict = dict(redCekanja)
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
    
    async def setup(self):
        primajPonasanje = self.PrimajPonude()
        self.add_behaviour(primajPonasanje)
        voziRedCekanjaPonasanje = self.VoziRedCekanja(period=5, start_at=datetime.datetime.now() + datetime.timedelta(seconds=10))
        self.add_behaviour(voziRedCekanjaPonasanje)
        print(f"Pokreće se {self.oznaka}")
        
    def encoder_taxi(self):
        return {'oznaka': self.oznaka, 'x': self.x, 'y': self.y, 'slobodan': self.slobodan, 'redCekanja': self.redCekanja}