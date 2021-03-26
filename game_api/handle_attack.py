

#################################################################
### Library for dealing with an attack and calculating damage ###
#################################################################

def execute_attack(attacker, defender, attack):
    print(f"{attacker.name.title()} is attacking {defender.name.title()} with {attack.name.title()}")
    attacker.RAM -= attack.cost
    print(f"{attacker.name.title()} spent {attack.cost} RAM and now has {attacker.RAM}")
    #damage = calculate_damage(attacker, defender, attack)

def calculate_damage(attacker, defender, attack):
    lvl_mod = get_lvl_mod(attacker, defender, attack)
    attacker_stat = get_attacker_stat(attacker, defender, attack)
    defender_stat = get_defender_stat(attacker, defender, attack)
    other = get_other_mod(attacker, defender, attack)
    damage = lvl_mod*attack.damage*attacker_stat/defender_stat*other
    return damage

def get_lvl_mod(attacker, defender, attack):
    pass

def get_attacker_stat(attacker, defender, attack):
    pass

def get_defender_stat(attacker, defender, attack):
    pass

def get_other_mod(attacker, defender, attack):
    pass


