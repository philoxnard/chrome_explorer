import random

from game_api.instantiate_party import get_base_phox, combine_phox_stats

##########################################
### Library for setting up an encounter ###
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
        # some function should probably be here to send info to the client
        # to draw everything
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
    # num_talents may change if the rate of talent acquisition changes
    for i in range(phox.level-1):
        index = random.randint(0, 1)
        upgrade_options = phox.upgrade_tree[i]
        phox.upgrades.append(upgrade_options[index])

# Gives the phox its temporary stats that will be used and manipulated in combat
# Looped through every phox in the party, as well as the wild phox
def set_temp_stats(phox):
    phox.temp_speed = phox.stats["speed"]
    phox.temp_cpow = phox.stats["cpow"]
    phox.temp_lpow = phox.stats["lpow"]
    phox.temp_csec = phox.stats["csec"]
    phox.temp_lsec = phox.stats["lsec"]
    phox.temp_rr = phox.stats["rr"]
    phox.temp_vis = phox.stats["vis"]