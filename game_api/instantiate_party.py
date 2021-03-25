from phox import Phox
from attack import Attack
from upgrades import get_upgrade_effects


################################################################################
### Library for instantiating phox classes for each phox in the user's party ###
################################################################################

# NOTE TO FUTURE SELF:
# It may seem like a hugely big and winding chore to separate instantiation into
# blueprint data fetching and collection data fetching, but this is paramount in
# case you want to tweak phox stats, talents, or literally anything in the future.
# Because every phox gets instantiated based on the blueprint in your database, any
# buffs or nerfs will carry over to every single instance of every single phox. 
# This will save you an absolutely colossal amount of time in the future.

# High level function for instantiating each phox in the party
# First goes through collection to find the phoxes for whom in_party is true
# Second, instantiates base versions of those phoxes
# Third, reads the user-specific information for each phox
# Finally, adds the user-specific info to each base phox
def instantiate_party(self):
    for phox, dictionary in self.player.collection.items():
        if dictionary["in_party"]:
            base_phox = get_base_phox(phox, self.phoxes)
            self.player.party.append(base_phox)
    for phox in self.player.party:
        get_collection_info(phox, self.player.collection, self.attacks, self.upgrades)


# Big long ugly function that gets an instance of a phox from the base blueprint
# Also called when instantiating wild phoxes
def get_base_phox(phox, phoxDB):
    new_phox = Phox()
    blueprint = phoxDB.find({"species": phox})
    for doc in blueprint:
        new_phox.species = doc["species"]
        new_phox.family = doc["family"]
        new_phox.base_stats = doc["base stats"]
        new_phox.stat_growth = doc["stat growth"]
        new_phox.upgrade_tree = doc["upgrade tree"]
        new_phox.attack_strings = doc["base attacks"]
        new_phox.upgrades = doc["base upgrades"]
        return new_phox

# Goes through the player's collection and grabs data for a
# phox in the current party.
# Also calls the function to combine the information
def get_collection_info(phox, collection, attackDB, upgradeDB):
    phox_info = collection[phox.species]
    phox.level = phox_info["level"]
    phox.experience = phox_info["experience"]
    # Get the array of indexes that determine which upgrades have been selected
    phox.upgrade_indexes = phox_info["upgrade indexes"]
    # The first index in this list is always 0 and must be removed
    phox.upgrade_indexes.pop(0)
    phox.nickname = phox_info["nickname"]
    phox.status = phox_info["status"]
    combine_phox_info(phox, attackDB, upgradeDB)

# High level function that contains all the information for 
# how to mix the blueprint data with the collection data
def combine_phox_info(phox, attackDB, upgradeDB):
    combine_phox_stats(phox)
    get_phox_upgrades(phox, upgradeDB)
    get_phox_attacks(phox, attackDB)

# Function to increment and implement changes to the stat block
def combine_phox_stats(phox):
    phox.stats["health"] = phox.base_stats["health"]+phox.level*phox.stat_growth["health"]
    phox.stats["speed"] = phox.base_stats["speed"]+phox.level*phox.stat_growth["speed"]
    phox.stats["cpow"] = phox.base_stats["cpow"]+phox.level*phox.stat_growth["cpow"]
    phox.stats["lpow"] = phox.base_stats["lpow"]+phox.level*phox.stat_growth["lpow"]
    phox.stats["csec"] = phox.base_stats["csec"]+phox.level*phox.stat_growth["csec"]
    phox.stats["lsec"] = phox.base_stats["lsec"]+phox.level*phox.stat_growth["lsec"]
    phox.stats["rr"] = phox.base_stats["rr"]+phox.level*phox.stat_growth["rr"]
    phox.stats["vis"] = phox.base_stats["vis"]+phox.level*phox.stat_growth["vis"]
    
    
# Function to give the phox its talents. Gets looped through entire party.
# Calls function from the talent.py module to flesh out the talents
# and actually make them mean something
def get_phox_upgrades(phox, upgradeDB):
    if phox.upgrade_indexes:
        for i in range(len(phox.upgrade_indexes)):
            index = phox.upgrade_indexes[i]
            upgrade_options = phox.upgrade_tree[i]
            phox.upgrades.append(upgrade_options[index])
    for upgrade in phox.upgrades:
        get_upgrade_effects(upgrade, phox, upgradeDB)

# This will take the string names of each attach, find those attacks in the attackDB,
# Then pass those attacks into a phox.attacks list. 
# Looped through entire party
# NOTE: Actual effects for attacks are instantiated and called during combat
def get_phox_attacks(phox, attackDB):
    for string in phox.attack_strings:
        attack = Attack()
        db_info = attackDB.find({"name": string})
        for doc in db_info:
            attack.name = doc["name"]
            attack.family = doc["family"]
            attack.style = doc["style"]
            attack.damage = doc["damage"]
            attack.cost = doc["cost"]
            attack.plain_text_effect = doc["plain text effect"]
            phox.attacks.append(attack)