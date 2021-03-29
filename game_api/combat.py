import random

from game_api.handle_attack import execute_attack

#########################################################
### Library for playing through every round of combat ###
#########################################################

# All of the randomization calculations can probably be simplified way down.


# Start of the combat chain
def combat(self):
    if self.wild_phox.disconnected:
        self.handle_experience(self.active_phoxes[0], self.wild_phox, self.player, self.players)
        self.state = "encounter cleanup"
    if self.state == "encounter":
        shutdown = check_shutdown(self.active_phoxes, self.player.party)
        if shutdown:
            self.player.shutdown = True
            self.state = "explore"
    if self.state == "encounter":
        swap_needed = is_swap_needed(self.active_phoxes)
        if swap_needed:
            swap_phoxes(self.active_phoxes, self.player.party)
    if self.state == "encounter":
        increment_speed(self.active_phoxes)

# Increment speed in the background
def increment_speed(phoxes):
    for phox in phoxes:
        phox.AS += phox.temp_speed
    check_for_turn(phoxes)

# Check to see if any phox has passed their speed threshold and gets to act
def check_for_turn(phoxes):
    for phox in phoxes:
        if phox.AS >= phox.AS_threshold:
            phox.can_act = True
    tie = check_for_tie(phoxes)
    if tie:
        settle_tie(phoxes)
    elif not phoxes[0].can_act and not phoxes[1].can_act:
        increment_speed(phoxes)
    else:
        for phox in phoxes:
            if phox.can_act:
                take_turn(phox, phoxes)
    

# Determines if both phoxes have hit their threshold at the same time
def check_for_tie(phoxes):
    if phoxes[0].can_act and phoxes[1].can_act:
        return True
    else:
        return False

# In the event of a tie, decides who gets to act first   
def settle_tie(phoxes):
    # Check for the photo_finish upgrade
    if phoxes[0].photo_finish == True and phoxes[1].photo_finish == False:
        print(phoxes[0].species + " has photo finish")
        take_turn(phoxes[0], phoxes)
        take_turn(phoxes[1], phoxes)
    elif phoxes[1].photo_finish == True and phoxes[0].photo_finish == False:
        print(phoxes[1].species + " has photo finish")
        take_turn(phoxes[1], phoxes)
        take_turn(phoxes[0], phoxes)
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
        take_turn(phoxes[0], phoxes)
        take_turn(phoxes[1], phoxes)
    if phoxes[1].AS > phoxes[0].AS:
        take_turn(phoxes[1], phoxes)
        take_turn(phoxes[0], phoxes)

def settle_tie_by_temp_speed(phoxes):
    if phoxes[0].temp_speed > phoxes[1].temp_speed:
        take_turn(phoxes[0], phoxes)
        take_turn(phoxes[1], phoxes)
    elif phoxes[1].temp_speed > phoxes[0].temp_speed:
        take_turn(phoxes[1], phoxes)
        take_turn(phoxes[0], phoxes)

# Randomize turn order for ties that can't be decided by speed or photo_finish
def randomize_turn(phoxes):
    num = random.randint(0, 1)
    print(f"{phoxes[num].name.title()} won the speed tie")
    take_turn(phoxes[num], phoxes)
    if num == 0:
        take_turn(phoxes[1], phoxes)
    elif num == 1:
        take_turn(phoxes[0], phoxes)

# High level architecture for what a turn looks like
def take_turn(phox, phoxes):
    if not phox.disconnected:
        update_RAM(phox)
        defender = get_defender(phox, phoxes)
        if phox.is_wild:
            wild_phox_take_turn(phox, defender)
        else:
            player_phox_takes_turn(phox, defender)
        phox.is_attacking = False
        phox.AS -= phox.AS_threshold
        phox.can_act = False
    print()
    ###########################
    # if phox.is_AI:          #
    # AI_phox_take_turn()     #
    # To be implemented later #
    ###########################

# Currently gets called only when a phox takes its turn
# May change to be called any time any turn is taken
# Or maybe even on every AS incrementation
def update_RAM(phox):
    if phox.RAM < phox.max_RAM:
        phox.RAM += phox.temp_rr
        if phox.RAM > phox.max_RAM:
            phox.RAM = phox.max_RAM
        print(f"{phox.name.title()} gained {phox.temp_rr} RAM and now has {phox.RAM}")

def get_defender(attacker, phoxes):
    attacker.is_attacking = True
    for phox in phoxes:
        if phox.is_attacking == False:
            return phox

def wild_phox_take_turn(phox, defender):
    random_max = len(phox.attacks) - 1
    num = random.randint(0, random_max)
    if phox.attacks[num].cost <= phox.RAM:
        attack = phox.attacks[num]
        execute_attack(phox, defender, attack)
    else:
        print("Not enough RAM")
        wild_phox_take_turn(phox, defender)
        
def player_phox_takes_turn(phox, defender):
    # This will all get redisigned when front end is in #
    for index, attack in enumerate(phox.attacks):
        print(f"[{index}]: {attack.name.title()}")
    num = int(input("Which attack do you pick? "))
    if phox.attacks[num].cost <= phox.RAM:
        attack = phox.attacks[num]
        execute_attack(phox, defender, attack)
    else:
        print("Not enough RAM")
        player_phox_takes_turn(phox, defender)

def check_shutdown(phoxes, party):
    if all(phox.disconnected for phox in party):
        print("You got disconnected!")
        return True

def is_swap_needed(active_phoxes):
    for index, phox in enumerate(active_phoxes):
        if not phox.is_wild:
            if phox.disconnected:
                return True

# When connected to front end, this will need a "forced" argument.
# If true, don't allow them to cancel the swap
def swap_phoxes(active_phoxes, party):
    active_phoxes.pop(0)
    for index, phox in enumerate(party):
        if not phox.disconnected:
            print(f"[{index}]: {phox.name.title()}")
    num = int(input("Which phox would you like to swap to? "))
    phox = party[num]
    active_phoxes.insert(0, phox)
