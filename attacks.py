

##################################################
### Library for generating effects for talents ###
##################################################

# Library called by intantiate_party.py

# Takes info from each attack dictionary and applies an actual effect
# based on the effect of the attack.

# This way, attacks can be updated by changing them in the database.
# However, this document must be updated each time an attack is made with 
# a brand new effect.

# NOTE: This will probably only actually ever get called in battle


def get_attack_effects(title, effect, phox):

    if title == "cha_boost":
        pass

    