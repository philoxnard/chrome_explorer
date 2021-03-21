import random

#############################################################################
### Library for determining if an encounter happens, and if so, what kind ###
#############################################################################

def determine_encounter(self):
    encounter = does_encounter_happen(self.encounter_frequency)
    if encounter:
        proceed = does_player_accept_encounter()
        if proceed:
            print("you fight a monster")
        else:
            print("you run from monster")
    else:
        print('no encounter')


def does_encounter_happen(frequency):
    chance = (random.randint(1, 100))
    if frequency > chance:
        return True

def does_player_accept_encounter():
    player_response = input("Run from encounter or engage? ")
    if player_response == "engage":
        proceed = True
    else:
        proceed = False
    return proceed