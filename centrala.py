from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import json
import initializer
from ast import literal_eval

class Centrala(Agent):
    class Radi(CyclicBehaviour):
        async def run(self):            
            msg = None
            msg = await self.receive(timeout=100)
            if msg:
                naredba = msg.get_metadata("intent")                
                if naredba == 'taxiji':
                    msg = msg.make_reply()
                    msg.body = self.agent.taxiji
                elif naredba == 'putnici':
                    msg = msg.make_reply()
                    msg.body = self.agent.putnici
                elif naredba == 'putnikRemove':
                    self.agent.putnici = json.loads(self.agent.putnici)
                    for i in range(len(self.agent.putnici)):
                        if str(self.agent.putnici[i]['oznaka']) == msg.body:
                            self.agent.putnici.pop(i)
                            break
                    self.agent.putnici = json.dumps(self.agent.putnici)
                elif naredba == 'taxiRemove':
                    self.agent.taxiji = json.loads(self.agent.taxiji)
                    for i in range(len(self.agent.taxiji)):
                        if str(self.agent.taxiji[i]['oznaka']) == msg.body:
                            self.agent.taxiji.pop(i)
                            break
                    if len(self.agent.taxiji) == 0:
                        print("Vise nema taksija. Sustav je gotov!")
                        await self.agent.stop()
                    self.agent.taxiji = json.dumps(self.agent.taxiji)
                elif naredba == 'taxijiUpdate':                    
                    body = json.loads(msg.body)
                    taxici = json.loads(self.agent.taxiji)                                      
                    for i in range(0, len(taxici)):
                        if taxici[i]['oznaka'] == body['oznaka']:
                            taxici[i]['redCekanja'] = body['redCekanja']
                            break
                    taxici = json.dumps(taxici)
                    self.agent.taxiji = taxici
                    return
            await self.send(msg)            
    
    async def setup(self):
        print(f"Stvorena je centrala! Postoji {len(self.taxiji)} taxija i {len(self.putnici)} putnika.")
        radiPonasanje = self.Radi()
        self.add_behaviour(radiPonasanje)
        self.taxiji = json.dumps(self.taxiji, default=initializer.Taxi.encoder_taxi, indent=4)
        self.putnici = json.dumps(self.putnici, default=initializer.Putnik.encoder_putnik, indent=4)