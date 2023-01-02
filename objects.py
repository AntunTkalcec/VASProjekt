class TaxiObject():
    def __init__(self, oznaka, x, y, slobodan):
        self.oznaka = oznaka
        self.x = x
        self.y = y
        self.slobodan = slobodan
        
class PutnikObject():
    def __init__(self, oznaka, x, y, x2, y2, vrijeme, zatrazioTaxi, nasaoTaxi):
        self.oznaka = oznaka
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.vrijeme = vrijeme
        self.zatrazioTaxi = zatrazioTaxi
        self.nasaoTaxi = nasaoTaxi