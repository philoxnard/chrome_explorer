from phox import Phox
from attack import Attack
from talents import get_talent_effects


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
        get_collection_info(phox, self.player.collection, self.attacks, self.talents)


# Big long ugly function that gets an instance of a phox from the base blueprint
# Will also likely be called when instantiating wild phoxes
def get_base_phox(phox, phoxDB):
    new_phox = Phox()
    blueprint = phoxDB.find({"species": phox})
    for doc in blueprint:
        new_phox.species = doc["species"]
        new_phox.family = doc["family"]
        stats = doc["base stats"]
        new_phox.strength = stats["STR"]
        new_phox.speed = stats["SPD"]
        new_phox.intelligence = stats["INT"]
        new_phox.constitution = stats["CON"]
        new_phox.spirit = stats["SPI"]
        new_phox.charisma = stats["CHA"]
        stat_growth = doc["stat growth"]
        new_phox.str_growth = stat_growth["STR"]
        new_phox.spd_growth = stat_growth["SPD"]
        new_phox.int_growth = stat_growth["INT"]
        new_phox.con_growth = stat_growth["CON"]
        new_phox.spi_growth = stat_growth["SPI"]
        new_phox.cha_growth = stat_growth["CHA"]
        talents = doc["talents"]
        new_phox.lvl2_talents = talents["level 2"]
        new_phox.lvl4_talents = talents["level 4"]
        new_phox.lvl6_talents = talents["level 6"]
        new_phox.lvl8_talents = talents["level 8"]
        new_phox.lvl10_talents = talents["level 10"]
        new_phox.talent_options =[new_phox.lvl2_talents, new_phox.lvl4_talents, new_phox.lvl6_talents, new_phox.lvl8_talents, new_phox.lvl10_talents]
        # NOTE: attack_strings is literally just a list of strings.
        #       These strings must then be put into attack db
        #       via get_phox_attacks
        new_phox.attack_strings = doc["base attacks"]
        new_phox.talents = doc["base talents"]
        return new_phox

# Goes through the player's collection and grabs data for a
# phox in the current party.
# Also calls the function to combine the information
def get_collection_info(phox, collection, attackDB, talentDB):
    phox_info = collection[phox.species]
    phox.level = phox_info["level"]
    phox.experience = phox_info["experience"]
    phox.talent_indexes = phox_info["talents"]
    # The first index in this list is always 0 and must be removed
    phox.talent_indexes.pop(0)
    phox.nickname = phox_info["nickname"]
    phox.status = phox_info["status"]
    combine_phox_info(phox, attackDB, talentDB)

# High level function that contains all the information for 
# how to mix the blueprint data with the collection data
def combine_phox_info(phox, attackDB, talentDB):
    combine_phox_stats(phox)
    get_phox_talents(phox, talentDB)
    get_phox_attacks(phox, attackDB)

# Function to increment and implement changes to the stat block
def combine_phox_stats(phox):
    added_str = (phox.level-1)*phox.str_growth
    phox.strength += added_str
    added_spd = (phox.level-1)*phox.spd_growth
    phox.speed += added_spd
    added_int = (phox.level-1)*phox.int_growth
    phox.intelligence += added_int
    added_con = (phox.level-1)*phox.con_growth
    phox.constitution += added_con
    added_spi = (phox.level-1)*phox.spi_growth
    phox.spirit += added_spi
    added_cha = (phox.level-1)*phox.cha_growth
    phox.charisma += added_cha
    phox.stats = [phox.strength, phox.speed, phox.intelligence, phox.constitution, phox.spirit, phox.charisma]

# Function to give the phox its talents. Gets looped through entire party.
# Calls function from the talent.py module to flesh out the talents
# and actually make them mean something
def get_phox_talents(phox, talentDB):
    if phox.talent_indexes:
        for i in range(len(phox.talent_indexes)):
            index = phox.talent_indexes[i]
            talent_options = phox.talent_options[i]
            phox.talents.append(talent_options[index])
    for talent in phox.talents:
        get_talent_effects(talent, phox, talentDB)

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