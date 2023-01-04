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
                    body = dict(msg.body)
                    cijena = body['cijena']
                    odredisteX = body['odredisteX']
                    odredisteY = body['odredisteY']
                    posiljatelj = msg.sender[0] + "@" + msg.sender[1]
                    redCekanja = self.agent.redCekanja
                    if posiljatelj not in redCekanja:
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
            if len(self.agent.redCekanja) > 0:
                msg = Message(
                    to=self.agent.redCekanja[0]['putnik'],
                    body="prihvacam",
                    metadata={
                        "intent":"ponuda",
                    }
                )
                await self.send(msg)
                
                odredisteX = self.agent.redCekanja[0]['odredisteX']
                odredisteY = self.agent.redCekanja[0]['odredisteY']
                cijena = self.agent.redCekanja[0]['cijena']
                print(f"{self.agent.oznaka} vozi putnika na {odredisteX}-{odredisteY}" + 
                      f"za {cijena} novcanih jedinica.")
                await asyncio.sleep(15)
                self.agent.x = odredisteX
                self.agent.y = odredisteY            
    
    async def setup(self):
        primajPonasanje = self.PrimajPonude()
        self.add_behaviour(primajPonasanje)
        voziRedCekanjaPonasanje = self.VoziRedCekanja(period=5, start_at=datetime.datetime.now() + datetime.timedelta(seconds=5))
        self.add_behaviour(voziRedCekanjaPonasanje)
        print(f"Pokreće se {self.oznaka}")
        
    def encoder_taxi(self):
        return {'oznaka': self.oznaka, 'x': self.x, 'y': self.y, 'slobodan': self.slobodan, 'redCekanja': self.redCekanja}