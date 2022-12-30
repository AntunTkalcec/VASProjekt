from spade.agent import Agent

class Centrala(Agent):
    async def setup(self):
        print(f"Stvorena je centrala! Postoji {len(self.taxiji)} taxija i {len(self.putnici)} putnika.")