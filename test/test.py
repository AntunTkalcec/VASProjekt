import spade


class PrviAgent(spade.agent.Agent):
    async def setup(self):
        print("PrviAgent: Pokrecem se!")


if __name__ == '__main__':
    a = PrviAgent("agent@localhost", "tajna")
    a.start()
    input("Press ENTER to exit. \n")
    a.stop()
    spade.quit_spade()