import random

#############################################################################
### Library for determining if an encounter happens, and if so, what kind ###
#############################################################################

def determine_encounter(self):
    encounter = does_encounter_happen(self.encounter_frequency)
    if encounter:
        proceed = does_player_accept_encounter()
        if proceed:
            which_phox_encountered(self.region, self.regions)
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

def which_phox_encountered(region, regions):
    frequency_sum = get_frequency_sum(region, regions)
    randint = random.randint(1, frequency_sum)
    encounter_list = get_encounter_list(region, regions, frequency_sum)
    encounter_index = randint-1
    phox_name = encounter_list[encounter_index]
    print(phox_name)
    return phox_name

def get_frequency_sum(region, regions):
    frequency_sum = 0
    for doc in regions.find({"region": region}):
        frequencies = doc["frequencies"]
        for key, value in frequencies.items():
            frequency_sum += value
    return frequency_sum

def get_encounter_list(region, regions, frequency_sum):
    frequency_list = []
    for doc in regions.find({"region": region}):
        frequencies = doc["frequencies"]
        for key, value in frequencies.items():
            for i in range(value):
                frequency_list.append(key)
    return frequency_list