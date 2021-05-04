import random

from game_api.instantiate_party import get_base_phox, combine_phox_info, get_phox_attacks
from upgrades import get_upgrade_effects

###########################################
### Library for setting up an encounter ###
###########################################

# NOTE: Something to decide later is whether to maintain the temp stats through 
#       swaps, or whether to have the temp stats reset every time a phox leaves/enters
#       the battlefield

# General handler for setting up a new encounter
def initialize_encounter(self):
    if self.state == "initialize encounter":
        # First, we get the blueprint for the base phox
        self.wild_phox = get_base_phox(self.phox_encountered, self.phoxes)
        # Next, get its level depending on where it was encountered
        self.wild_phox.level = get_wild_phox_level(self.region, self.regions)
        # Then, increment the phox based on its assigned level
        combine_phox_info(self.wild_phox, self.attacks, self.upgrades, self.families)
        # Get the randomized upgrades for the wild phox
        get_phox_upgrades(self.wild_phox)
        # Get the upgrade effects into the wild phox
        for upgrade in self.wild_phox.upgrades:
            get_upgrade_effects(upgrade, self.wild_phox, self.upgrades)
        # Get the actual attack effects into the wild phox
        get_phox_attacks(self.wild_phox, self.attacks, self.families)
        # Set the temp stats for the wild phox
        set_temp_stats(self.wild_phox)
        # Set the name for the wild phox
        self.wild_phox.name = self.wild_phox.species
        # Make sure the game knows that the phox is wild
        self.wild_phox.is_wild = True
        for attack in self.wild_phox.attacks:
            print(attack.name)
        # Set the temp stats, RAM, and name for the phoxes in your party
        # Also resets some other aspects of combat
        for phox in self.player.party:
            reset_phox(phox)
        self.active_phoxes = get_active_phoxes(self.player.party, self.wild_phox)
        # some function should probably be here to send info to the client
        # to draw everything
        print(f"You found a level {self.wild_phox.level} {self.wild_phox.name.title()}")
        print(f"Go get 'em, {self.player.party[0].name.title()}!")
        


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
def get_phox_upgrades(phox):
    # num_talents may change if the rate of talent acquisition changes
    for i in range(phox.level):
        index = random.randint(0, 1)
        upgrade_options = phox.upgrade_tree[i]
        phox.upgrades.append(upgrade_options[index].name)
        print(phox.upgrades)

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

def get_active_phoxes(party, wild_phox):
    for phox in party:
        if not phox.disconnected:
            return [phox, wild_phox]

def reset_phox(phox):
    set_temp_stats(phox)
    phox.name = phox.species
    phox.RAM = phox.max_RAM
    phox.AS = phox.base_AS
    phox.can_act = False
    phox.is_attacking = False
    phox.turns_active = 0
    phox.first_attack = True

    # Status effects
    phox.turns_node = 0

    # Attack specific modifiers
    phox.repost_mod = 1
    phox.PoW_mod = 1

    print(f'phox status is {phox.status}')