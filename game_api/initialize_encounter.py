import random

from game_api.instantiate_party import get_base_phox

##########################################
### Library for settig up an encounter ###
##########################################

# General handler for setting up a new encounter
def initialize_encounter(self):
    if self.state == "initialize_encounter":
        self.wild_phox = get_base_phox(self.phox_encountered, self.phoxes)
        level = get_wild_phox_level(self.region, self.regions)
        level_up_phox(self.wild_phox, level)
        set_temp_stats(self.wild_phox)
        for phox in self.player.party:
            set_temp_stats(phox)
        self.state = "encounter"


# Get the level range from the region, pick a random int in the range,
# and return the int.
def get_wild_phox_level(region, regionsDB):
    region_info = regionsDB.find({"region": region})
    for doc in region_info:
        array = doc["level range"]
        lvl_min = array[0]
        lvl_max = array[1]
        level = random.randint(lvl_min, lvl_max)
    return level

# Increment the phox's stats according to its level and randomize its talents
def level_up_phox(phox, level):
    pass

# Gives the phox its temporary stats that will be used and manipulated in combat
# Looped through every phox in the party, as well as the wild phox
def set_temp_stats(phox):
    pass