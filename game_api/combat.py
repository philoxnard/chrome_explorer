import random

from game_api.handle_attack import execute_attack

#########################################################
### Library for playing through every round of combat ###
#########################################################

# Start of the combat chain
def combat(self):
    self.combat_info_dict = None
    if check_shutdown(self.player.party):
        self.player.shutdown = True
        self.state = "explore"
    elif self.wild_phox.disconnected:
        self.handle_experience(self.active_phoxes[0], self.wild_phox, self.player, self.players)
        self.state = "encounter cleanup"
        self.encounter_cleanup
    elif is_swap_needed(self.active_phoxes):
        swap_phoxes(self.active_phoxes, self.player.party)
    else:
        phox = check_for_turn(self.active_phoxes)
        if phox:
            if phox.is_wild:
                self.combat_info_dict = wild_phox_take_turn(phox, self.active_phoxes)
            else:
                self.combat_state = "waiting" 
        else:
            increment_speed(self.active_phoxes)
            combat(self)

def execute_player_attack(self):
    self.combat_info_dict = player_phox_takes_turn(self.active_phoxes, self.player_attack)
    if self.combat_info_dict:
        self.combat_state = None
        self.player_attack = None

# Increment speed in the background
def increment_speed(phoxes):
    for phox in phoxes:
        phox.AS += phox.temp_speed
        print(f"{phox.name} increments to {phox.AS} AS")
    

# Check to see if any phox has passed their speed threshold and gets to act
def check_for_turn(phoxes):
    for phox in phoxes:
        if phox.AS >= phox.AS_threshold:
            print(f'{phox.name} can act')
            phox.can_act = True
    tie = check_for_tie(phoxes)
    # If both phoxes can act
    if tie:
        phox = settle_tie(phoxes)
        return phox
    # If neither phox can act
    elif not phoxes[0].can_act and not phoxes[1].can_act:
        return None
    
    # If one phox can act
    else:
        for phox in phoxes:
            if phox.can_act:
                return phox
    

# Determines if both phoxes have hit their threshold at the same time
def check_for_tie(phoxes):
    if phoxes[0].can_act and phoxes[1].can_act:
        return True
    else:
        return False

# In the event of a tie, decides who gets to act first   
def settle_tie(phoxes):
    if not phoxes[0].AS == phoxes[1].AS:
        phox = settle_tie_by_AS(phoxes)
    elif not phoxes[0].temp_speed == phoxes[1].temp_speed:
        phox = settle_tie_by_temp_speed(phoxes)
    else:
        phox = randomize_turn(phoxes)
    return phox

def settle_tie_by_AS(phoxes):
    if phoxes[0].AS > phoxes[1].AS:
        return phoxes[0]
    if phoxes[1].AS > phoxes[0].AS:
        return phoxes[1]

def settle_tie_by_temp_speed(phoxes):
    if phoxes[0].temp_speed > phoxes[1].temp_speed:
        return phoxes[0]
    elif phoxes[1].temp_speed > phoxes[0].temp_speed:
        return phoxes[1]

# Randomize turn order for ties that can't be decided by speed or photo_finish
def randomize_turn(phoxes):
    num = random.randint(0, 1)
    print(f"{phoxes[num].name.title()} won the speed tie")
    return phoxes[num]

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

def upkeep(phox, phoxes):
    defender = get_defender(phox, phoxes)
    return defender

def wild_phox_take_turn(phox, phoxes):
    # if all(not phox.disconnected for phox in phoxes):
    defender = upkeep(phox, phoxes)
    random_max = len(phox.attacks) - 1
    num = random.randint(0, random_max)
    if phox.attacks[num].cost <= phox.RAM:
        attack = phox.attacks[num]
        info_dict = execute_attack(phox, defender, attack)
        phox.is_attacking = False
        phox.AS -= phox.AS_threshold
        phox.can_act = False
        update_RAM(phox)
        return info_dict
    else:
        print("Not enough RAM")
        wild_phox_take_turn(phox, phoxes)
        
def player_phox_takes_turn(phoxes, attack_name):
    # if all(not phox.disconnected for phox in phoxes):
    print(attack_name)
    for phox in phoxes:
        if not phox.is_wild:
            defender = upkeep(phox, phoxes)
            for attack in phox.attacks:
                if attack.name == attack_name:
                    print(f'trying attack {attack.name}')
                    if attack.cost<= phox.RAM:
                        print(f'executing attack {attack.name}')
                        info_dict = execute_attack(phox, defender, attack)
                        update_RAM(phox)
                        phox.is_attacking = False
                        phox.AS -= phox.AS_threshold
                        phox.can_act = False
                        return info_dict
                    else:
                        print("Not enough RAM")
                        return None

def check_shutdown(party):
    if all(phox.disconnected for phox in party):
        print("You got Shut Down!")
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
