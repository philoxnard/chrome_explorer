import random

#############################################################################
### Library for determining if an encounter happens, and if so, what kind ###
#############################################################################

# General handler for determining the encounter for each trot
def determine_encounter(self):
    encounter = does_encounter_happen(self.encounter_frequency)
    if encounter:
        proceed = does_player_accept_encounter()
        if proceed:
            self.phox_encountered = which_phox_encountered(self.region, self.regions)
            self.state = "initialize_encounter"
            print(self.phox_encountered)
        else:
            print("you run from monster")
    else:
        print('no encounter')

# Takes self.encounter_frequency and determines if an encounter happens at all
def does_encounter_happen(frequency):
    chance = (random.randint(1, 100))
    if frequency > chance:
        return True

# Takes user input to determine to run from encounter or to engage
def does_player_accept_encounter():
    player_response = input("Run from encounter or engage? ")
    if player_response == "engage":
        proceed = True
    else:
        proceed = False
    return proceed

# High level cuntion to determine which phox gets encountered based on region
def which_phox_encountered(region, regions):
    frequency_sum = get_frequency_sum(region, regions)
    randint = random.randint(1, frequency_sum)
    encounter_list = get_encounter_list(region, regions, frequency_sum)
    encounter_index = randint-1
    phox_name = encounter_list[encounter_index]
    return phox_name

# Sums up the total frequency points in the given region
def get_frequency_sum(region, regions):
    frequency_sum = 0
    for doc in regions.find({"region": region}):
        frequencies = doc["frequencies"]
        for key, value in frequencies.items():
            frequency_sum += value
    return frequency_sum

# Creates a list of potential encounters from the given region
def get_encounter_list(region, regions, frequency_sum):
    frequency_list = []
    for doc in regions.find({"region": region}):
        frequencies = doc["frequencies"]
        for key, value in frequencies.items():
            for i in range(value):
                frequency_list.append(key)
    return frequency_list