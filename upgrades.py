

##################################################
### Library for generating effects for talents ###
##################################################

# Library called by intantiate_party.py
# This entire thing is literally just one single function that is responsible
# for altering every single talent

# Takes info from each talent dictionary and applies an actual effect
# based on the effect of the talent.

# This way, talents can be updated by changing them in the database.
# However, this document must be updated each time a talent is made with
# a brand new effect.

"""
A quick reference dictionary of effects:

new_attack - adds the attack to the phox's list of attacks
stat_boost - adds a flat boost to the phox's stats
stat_boost_after_attack - adds a flat boost to the phox's temp stats after each time they attack
stat_mod - multiply the phox's stat by that amount
NEEDS WORK immunity - gives immunity to the noted status effect OR attack family
family_mod - multiply the damage the phox deals with that family of attack
adv/dadv/weak/res_mod - change the effectiveness of weakness/resistances/advantage/disadvantage for that phox
NEEDS WORK favored_foe - add that family to the phox's favored foe list

"""

def get_upgrade_effects(upgrade_string, phox, upgradeDB):
    upgrade = upgradeDB.find({"name": upgrade_string})
    for doc in upgrade:
        for title, effect in doc["effect"].items():

            if title == "vis_boost":
                phox.stats["vis"] += effect

            if title == "lpow_boost":
                phox.stats["lpow"] += effect

            if title == "cpow_boost":
                phox.stats["cpow"] += effect

            if title == "csec_boost":
                phox.stats["csec"] += effect

            if title == "lsec_boost":
                phox.stats["lsec"] += effect

            if title == "hp_boost":
                phox.max_health += effect
                phox.stats["health"] += effect

            if title == "spd_boost":
                phox.stats["speed"] += effect

            if title == "res_mod":
                phox.resistance_mod *= effect

            if title == "weak_mod":
                phox.weakness_mod *= effect

            if title == "adv_mod":
                phox.advantage_mod *= effect

            if title == "dadv_mod":
                phox.disadvantage_mod *= effect

            if title == "new_attack":
                phox.attack_strings.append(effect)

            if title == "exp_mod":
                effect /= 100
                phox.exp_mod *= effect

            if title == "AS_boost":
                phox.base_AS += effect

            if title == "spd_mod":
                phox.stats["speed"] = int(phox.stats["speed"] * effect)

            if title == "data_mod":
                phox.data_mod *= effect
                print(phox.data_mod)

            if title == "copypaste":
                phox.copypaste = True

            if title == "regenerate":
                phox.regenerate += effect

            if title == "null_field":
                phox.null_field = True

            if title == "immunity":
                for status in effect:
                    phox.immunities.append(status)

            