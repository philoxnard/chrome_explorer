import random

from game_api.handle_attack import execute_attack

#########################################################
### Library for playing through every round of combat ###
#########################################################

# Start of the combat chain
def combat(self):
    """
    An important thing to understand about this function is that it gets called whenever
    the player clicks the "continue" button. That means that combat might "be over" before
    the button even gets clicked - i.e. if a phox has already disconnected, so we check to
    see if combat should end BEFORE we even get into the real meat of the combat code.
    """

    # Create an empty dictionary that will store information displayed to the user
    self.combat_info_dict = {}

    # If the wild phox has disconnected, we process the end of the encounter
    if self.wild_phox.disconnected:

        processWildPhoxDisconnection(self)

    # If the player's phox has disconnected, we process that
    elif self.active_phoxes[0].disconnected:

        processPlayerPhoxDisconnection(self)

    else:

        # We check to see if there's a phox that's eligible to take its turn
        phox = check_for_turn(self.active_phoxes)
        if phox:
            if phox.is_wild:
                self.combat_info_dict = wild_phox_take_turn(phox, self.active_phoxes)

                self.check_disconnect_and_shutdown()

            else:
                self.combat_state = "waiting"

            for phox in self.active_phoxes:
                phox.incrementTurns()

        # If neither Phox is eligible to take a turn, we increment AS and repeat the combat loop
        else:
            increment_speed(self.active_phoxes)
            self.combat()

    if self.combat_info_dict:
        print(self.combat_info_dict)

def execute_player_attack(self):
    self.combat_info_dict = player_phox_takes_turn(self.active_phoxes, self.player_attack)
    self.check_disconnect_and_shutdown()

    # I think we need to check to see if the player phox d/c's on your own turn
    # because it could die on its own turn to an effect like Node
    if self.active_phoxes[0].disconnected:
        processPlayerPhoxDisconnection

    # Not sure exactly what this is for but it seems necessary
    if not "swap needed" in self.combat_info_dict:
        self.combat_state = None
        self.player_attack = None

def check_disconnect_and_shutdown(self):

    if all(phox.disconnected for phox in self.player.party):
        print("Shutdown!")
        self.player.shutdown = True
        self.combat_info_dict["swap needed"] = \
                "You have shut down! Hit 'Run' and go to \
                Phoxtrot.com to heal your Phoxes"

    elif self.active_phoxes[0].disconnected:
        processPlayerPhoxDisconnection()


# Increment speed in the background
def increment_speed(phoxes):

    for phox in phoxes:
        print(f"{phox.name} currently has {phox.AS} AS, with a speed stat of {phox.temp_speed}")
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
        active_phox = settle_tie(phoxes)
        return active_phox
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

def processWildPhoxDisconnection(game):

    game.handle_experience(game.active_phoxes[0], game.wild_phox, game.player, game.players)
    game.encounter_cleanup()

def processPlayerPhoxDisconnection(game):

    game.combat_state = "waiting"
    game.combat_info_dict = {"swap needed": "Your phox has disconnected. \
                                            Swap to a different phox in your party."}

# Currently gets called only when a phox takes its turn
# May change to be called any time any turn is taken
# Or maybe even on every AS incrementation
# NOTE: This should be a method of the Phox class
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
    attack = determine_wild_phox_attack(phox, defender)
    info_dict = execute_attack(phox, defender, attack)

    phox.cleanupAttack()

    update_RAM(phox)
    print('made it to the end of the wild_phoxs turn')
    if defender.disconnected:
        info_dict["swap needed"] = "Your phox has disconnected. \
                                    Swap to a different phox in your party."
    return info_dict

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

                        phox.cleanupAttack()

                        print('made it to the end of the players turn')
                        return info_dict
                    else:
                        print("Not enough RAM")
                        # return None

def check_shutdown(party):
    if all(phox.disconnected for phox in party):
        print("You got Shut Down!")
        return True

def is_swap_needed(active_phoxes):
    print("detecting if a swap is needed")
    for phox in active_phoxes:
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

def determine_wild_phox_attack(attacker, defender):
    attack = check_zero_cost_attack(attacker, defender)
    if attack:
        print(f'returning {attack}')
        return attack
    attack = not_zero_cost_attack(attacker, defender)
    print(f'returning {attack}')
    return attack

def check_zero_cost_attack(attacker, defender):
    attack_costs = []
    for attack in attacker.attacks:
        print(f'{attack.name} costs {attack.cost}')
        attack_costs.append(attack.cost)
    attack_costs.sort()
    print(f' the attack costs are: {attack_costs}')
    print(f'attacker ram: {attacker.RAM}')
    if attacker.RAM < attack_costs[1]:
        for attack in attacker.attacks:
            if attack.cost == 0:
                return attack

def not_zero_cost_attack(attacker, defender):
    attack_chosen = False
    while attack_chosen == False:
        potential_attacks = []
        for attack in attacker.attacks:
            if attack.cost > 0:
                potential_attacks.append(attack)
        random_max = len(potential_attacks) - 1
        num = random.randint(0, random_max)
        attack = potential_attacks[num]
        if attacker.RAM >= attack.cost:
            print('selected attack ' + attack.name.title())
            attack_chosen = True
            return attack
        else:
            print('Not enough RAM')
        # not_zero_cost_attack(attacker, defender)

    