

##################################################
### Library for generating effects for talents ###
##################################################

# Library called by intantiate_party.py
# This entire thing is literally just one single function that is responsible
# for altering every single talent

# Need to figure out if there's a way to do this from the talentDB isntead of 
# here in a python file

# Its eval() !!!!
# store effects as strings in an array
# loop through the array and eval() each string

def get_talent_effects(talent, phox):
    if talent == "hard worker":
        phox.exp_multiplier = 1.5
    if talent == "charmer":
        phox.charisma += 20
        phox.attack_strings.append("charm")
