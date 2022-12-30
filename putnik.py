from spade.agent import Agent

class Putnik(Agent):        
    async def setup(self):
        print(f"Stvoren je putnik {self.oznaka}, na adresi {self.x}-{self.y}, sa ciljem {self.x2}-{self.y2}!")