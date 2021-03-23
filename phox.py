class Phox:
    """
    A class to model a phox
    """

    def __init__(self):
        self.species = ""
        self.nickname = ""
        self.level = 0
        self.experience = 0
        self.strength = 0
        self.speed = 0
        self.intelligence = 0
        self.constitution = 0
        self.spirit = 0
        self.charisma = 0
        self.status = None
        self.talents = []
        self.attacks = []
        self.exp_mod = 1

        # These stats are set equal to the phox's actual stat when combat starts
        # and they are then manipulated and used in that single combat
        self.temp_str = 0
        self.temp_spd = 0
        self.temp_int = 0
        self.temp_con = 0
        self.temp_spi = 0
        self.temp_cha = 0

        self.photo_finish = False
