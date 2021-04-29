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

        self.player_art= ""
        self.enemy_art = ""

        self.max_health = 0
        self.max_RAM = 100
        self.RAM = self.max_RAM
        self.base_stats = {}
        self.stat_growth = {}
        self.upgrade_indexes = []
        self.upgrade_tree = []
        self.upgrade_tree_strings = []
        self.attack_strings = []
        self.upgrades = []
        self.base_upgrades = []

        self.stats = {}

        self.status = None

        # Populated with the actual class instances, not just strings
        self.attacks = []

        # Modifed by some attacks, then set back to 1 after the attack resolves
        self.temp_damage_mod = 1

        # Set to true when a phox takes their turn, helps in passing information
        # to the functions that calculate damage
        self.is_attacking = False

        self.status = None

        self.AS = 0
        self.base_AS = 0
        self.AS_threshold = 100

        # Used to help determine who goes in the case of speed ties
        self.can_act = False

        # Set to false after the phox makes its first attack, set to True
        # if the phox switches out
        self.first_attack = True

        # When a phox loses all of its HP, it disconnects
        self.disconnected = False

        # Name is given to a phox based on its nickname or species if its tame or wild
        # Used in battle for testing and prob also for text display later
        self.name = ""

        # Modifier on exp gained, some upgrades will modify this
        self.exp_mod = 1

        # Modifiers for specific family attacks
        self.data_mod = 1

        # Set to true whenever a wild phox is instantiated
        self.is_wild = False

        ##### List of possible passive upgrade abilities 
        self.copypaste = False

        ##### List of possible mods for specific attakcs
        self.repost_mod = 1
        

    def serialize(self):
        stats = self.stats
        stats["max health"]=self.max_health
        family = ""
        for fam in self.family:
            family += fam.title()
        return {
            "species": self.species.title(),
            "nickname": self.nickname.title(),
            "family": self.family,
            "stats": stats,
            "level": self.level,
            "upgrade indexes": self.upgrade_indexes,
            "player art": self.player_art,
            "enemy art": self.enemy_art}
