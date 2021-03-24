

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

def get_upgrade_effects(upgrade_string, phox, upgradeDB):
    upgrade = upgradeDB.find({"name": upgrade_string})
    for doc in upgrade:
        for title, effect in doc["effect"].items():

            if title == "win_speed_tie":
                phox.photo_finish = effect

            if title == "vis_boost":
                phox.stats["vis"] += effect
            
            if title == "new_attack":
                phox.attack_strings.append(effect)

            if title == "exp_mod":
                effect /= 100
                phox.exp_mod *= effect

            