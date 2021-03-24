class Phox:
    """
    A class to model a phox
    """

    def __init__(self):
        self.species = "asdf"
        self.family = ""
        self.nickname = ""
        self.level = 0
        self.experience = 0

        self.health = 0
        self.RAM = 100
        self.base_stats = {}
        self.stat_growth = {}
        self.upgrade_tree = {}
        self.attack_strings = []
        self.upgrades = []

        self.attacks = []

        self.status = None
        self.exp_mod = 1

        # Set to true whenever a wild phox is instantiated
        self.is_wild = False

        self.photo_finish = False
