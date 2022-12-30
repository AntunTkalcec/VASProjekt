from spade.agent import Agent
import random
from spade.message import Message
from spade.template import Template
from spade import quit_spade

from time import sleep

class Taxi(Agent):
    async def setup(self):
        print(f"Pokreće se Taxi {self.oznaka}")