import random

from game_api.instantiate_party import get_base_phox, combine_phox_stats

##########################################
### Library for settig up an encounter ###
##########################################

# General handler for setting up a new encounter
def initialize_encounter(self):
    if self.state == "initialize_encounter":
        self.wild_phox = get_base_phox(self.phox_encountered, self.phoxes)
        self.wild_phox.level = get_wild_phox_level(self.region, self.regions)
        combine_phox_stats(self.wild_phox)
        get_phox_talents(self.wild_phox)
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

# Randomize talents according to the phox's level
def get_phox_talents(phox):
    print(phox.level)
    num_talents = int(phox.level/2)
    for i in range(num_talents):
        index = random.randint(0, 1)
        talent_options = phox.talent_options[i]
        phox.talents.append(talent_options[index])

# Gives the phox its temporary stats that will be used and manipulated in combat
# Looped through every phox in the party, as well as the wild phox
def set_temp_stats(phox):
    pass