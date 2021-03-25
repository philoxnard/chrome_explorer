import random


#########################################################
### Library for playing through every round of combat ###
#########################################################

# All of the randomization calculations can probably be simplified way down.

# Start of the combat chain
def combat(self):
    if self.state == "encounter":
        increment_speed(self.active_phoxes)

# Increment speed in the background
def increment_speed(phoxes):
    for phox in phoxes:
        phox.AS += phox.temp_speed
        # All this stuff can get removed later, just here for testing:
        if phox.is_wild:
            var = "Wild"
        elif not phox.is_wild:
            var = "Your"
        print(f"{var} {phox.name.title()} has incremented to {phox.AS} AS")
    check_for_turn(phoxes)

# Check to see if any phox has passed their speed threshold and gets to act
def check_for_turn(phoxes):
    for phox in phoxes:
        if phox.AS >= phox.AS_threshold:
            phox.can_act = True
            print(f"{phox.name.title()} has hit its AS threshold")
    tie = check_for_tie(phoxes)
    if tie:
        settle_tie(phoxes)
    else:
        for phox in phoxes:
            if phox.can_act:
                take_turn(phox)
    increment_speed(phoxes)

# Determines if both phoxes have hit their threshold at the same time
def check_for_tie(phoxes):
    if phoxes[0].can_act and phoxes[1].can_act:
        print("we have a speed tie")
        return True
    else:
        print("no speed tie detected")
        return False

# In the event of a tie, decides who gets to act first   
def settle_tie(phoxes):
    # Check for the photo_finish upgrade
    if phoxes[0].photo_finish == True and phoxes[1].photo_finish == False:
        print(phoxes[0].species + " has photo finish")
        take_turn(phoxes[0])
        take_turn(phoxes[1])
    elif phoxes[1].photo_finish == True and phoxes[0].photo_finish == False:
        print(phoxes[1].species + " has photo finish")
        take_turn(phoxes[1])
        take_turn(phoxes[0])
    # If both or neither phoxes have photo_finish, pick by AS, then temp_speed, then random
    else:
        if not phoxes[0].AS == phoxes[1].AS:
            settle_tie_by_AS(phoxes)
        elif not phoxes[0].temp_speed == phoxes[1].temp_speed:
            settle_tie_by_temp_speed(phoxes)
        else:
            randomize_turn(phoxes)

def settle_tie_by_AS(phoxes):
    if phoxes[0].AS > phoxes[1].AS:
        take_turn(phoxes[0])
        take_turn(phoxes[1])
    if phoxes[1].AS > phoxes[0].AS:
        take_turn(phoxes[1])
        take_turn(phoxes[0])

def settle_tie_by_temp_speed(phoxes):
    if phoxes[0].temp_speed > phoxes[1].temp_speed:
        take_turn(phoxes[0])
        take_turn(phoxes[1])
    elif phoxes[1].temp_speed > phoxes[0].temp_speed:
        take_turn(phoxes[1])
        take_turn(phoxes[0])

# Randomize turn order for ties that can't be decided by speed or photo_finish
def randomize_turn(phoxes):
    num = random.randint(0, 1)
    print(f"the random index is: {num}")
    take_turn(phoxes[num])
    if num == 0:
        take_turn(phoxes[1])
    elif num == 1:
        take_turn(phoxes[0])

# High level architecture for what a turn looks like
def take_turn(phox):
    if phox.is_wild:
        wild_phox_take_turn(phox)
    else:
        player_phox_takes_turn(phox)
    phox.AS -= phox.AS_threshold
    phox.can_act = False
    print(f"After decrementing, phox has {phox.AS} AS")
    # function to check if fight is over
    ###########################
    # if phox.is_AI:          #
    # AI_phox_take_turn()     #
    # To be implemented later #
    ###########################

def wild_phox_take_turn(phox):
    random_max = len(phox.attacks) - 1
    num = random.randint(0, random_max)
    # if phox.attacks[num].cost <= phox.RAM:
    print("Performing wild phox attack")
        
def player_phox_takes_turn(phox):
    # This will all get redisigned when front end is in #############
    for index, attack in enumerate(phox.attacks):                   #
        print(f"[{index}]: {attack.name.title()}")                  #
    num = int(input("Which attack do you pick? "))                  #
    # print("Or, type 'run' or 'swap' to do either of those")       #
    print(f"Executing attack: {phox.attacks[num].name.title()}")    #
    #################################################################