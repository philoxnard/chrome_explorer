class Phox:
    """
    A class to model a phox
    """

    def __init__(self):
        self.species = ""
        self.family = ""
        self.nickname = ""
        self.level = 0
        self.experience = 0

        self.health = 0
        self.RAM = 100
        self.base_stats = {}
        self.stat_growth = {}
        self.upgrade_indexes = []
        self.upgrade_tree = {}
        self.attack_strings = []
        self.upgrades = []

        self.stats = {}

        self.attacks = []

        self.status = None

        self.AS = 0
        self.AS_threshold = 100
        self.can_act = False
        # Name is given to a phox based on its nickname or species if its tame or wild
        # Used in battle for testing and prob also for text display later
        self.name = ""

        self.exp_mod = 1

        # Set to true whenever a wild phox is instantiated
        self.is_wild = False

        self.photo_finish = False
