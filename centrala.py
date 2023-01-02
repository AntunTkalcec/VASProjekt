import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
import json
import asyncio
import initializer

class Centrala(Agent):
    class Radi(CyclicBehaviour):
        async def run(self):
            msg = None
            msg = await self.receive(timeout=100)
            if msg:
                naredba = msg.get_metadata("intent")                
                if naredba == 'taxiji':
                    msg = msg.make_reply()
                    msg.body = json.dumps(self.agent.taxiji, default=initializer.Taxi.encoder_taxi, indent=4)
                elif naredba == 'putnici':
                    msg = msg.make_reply()
                    msg.body = json.dumps(self.agent.putnici, default=initializer.Putnik.encoder_putnik, indent=4)
            await self.send(msg)            
    
    async def setup(self):
        print(f"Stvorena je centrala! Postoji {len(self.taxiji)} taxija i {len(self.putnici)} putnika.")
        radiPonasanje = self.Radi()
        self.add_behaviour(radiPonasanje)