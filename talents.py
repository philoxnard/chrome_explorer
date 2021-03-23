

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

def get_talent_effects(talent_string, phox, talentDB):
    talent = talentDB.find({"name": talent_string})
    for doc in talent:
        for title, effect in doc["effect"].items():

            if title == "cha_boost":
                phox.charisma += effect
            
            if title == "new_attack":
                phox.attack_strings.append(effect)

            if title == "exp_mod":
                effect /= 100
                phox.exp_mod *= effect
