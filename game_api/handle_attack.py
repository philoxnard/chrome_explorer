import random

from attacks import pre_attack_effect, post_attack_effect


#################################################################
### Library for dealing with an attack and calculating damage ###
#################################################################

def execute_attack(attacker, defender, attack):
    print(attacker)
    print(defender)
    print(attack)
    pre_effect_dict = pre_attack_effect(attacker, defender, attack)
    print(f"{attacker.name.title()} is attacking {defender.name.title()} with {attack.name.title()}")
    attacker.RAM -= attack.cost
    print(f"{attacker.name.title()} spent {attack.cost} RAM and now has {attacker.RAM}")
    damage = int(calculate_damage(attacker, defender, attack))
    deal_damage(damage, attacker, defender)
    post_effect_dict = post_attack_effect(attacker, defender, attack)
    if attacker.is_wild:
        ownership = "Wild"
    else:
        ownership = "Your"
    info_dict = {
        "ownership": ownership,
        "attack": attack.name.title(),
        "damage": damage,
        "attacker": attacker.name.title(),
        "defender": defender.name.title(),
    }
    info_dict = {**info_dict, **pre_effect_dict, **post_effect_dict}
    attacker.temp_damage_mod = 1
    return info_dict
    

def calculate_damage(attacker, defender, attack):
    global_mod = 9
    random_mod = get_random_mod()
    lvl_mod = get_lvl_mod(attacker)
    attacker_stat = get_attacker_stat(attacker, defender, attack)
    defender_stat = get_defender_stat(attacker, defender, attack)
    other = get_other_mod(attacker, defender, attack)
    damage = lvl_mod*attack.damage*attacker_stat/defender_stat*other/global_mod*random_mod
    return damage

def get_random_mod():
    num = random.randint(85, 115)
    num = float(num/100)
    return num

def get_lvl_mod(attacker):
    mod = 1
    return mod


def get_attacker_stat(attacker, defender, attack):
    if attack.style == "local":
        attacker_stat = attacker.temp_lpow
    elif attack.style == "cloud":
        attacker_stat = attacker.temp_cpow
    else:
        attacker_stat = 1
    return attacker_stat

# This will eventually get conditionals like:
# if attack.effect == "hits_local":
#   defender_stat = defender.temp_lsec
def get_defender_stat(attacker, defender, attack):
    if attack.style == "local":
        defender_stat = defender.temp_lsec
    elif attack.style == "cloud":
        defender_stat = defender.temp_csec
    else:
        defender_stat = 1
    return defender_stat

def get_other_mod(attacker, defender, attack):
    family_mod = get_family_mod(attacker, defender, attack)
    STAB = get_STAB(attacker, attack)
    special_family_mod = get_special_family_mod(attacker, attack)
    mod = float(STAB*family_mod*attacker.temp_damage_mod*special_family_mod)
    return mod

def get_family_mod(attacker, defender, attack):
    mod = float(1)
    for family in defender.family:
        if family in attack.advantages:
            mod *= 2
        if family in attack.disadvantages:
            mod /= 2
        if family in attack.zero_effects:
            mod *= 0
    return mod

def get_STAB(attacker, attack):
    mod = float(1)
    if attack.family in attacker.family:
        mod *= 1.5
    return mod

def get_special_family_mod(attacker, attack):
    mod = float(1)
    if attack.family == "data":
        mod *= attacker.data_mod
        [print('boosting Data attack')]
    return mod


def deal_damage(damage, attacker, defender):
    print(f"The attack dealt {damage} damage")
    defender.stats["health"] -= damage
    if defender.stats["health"] < 0:
        defender.stats["health"] = 0
    print(f"{defender.name.title()} has {defender.stats['health']} health remaining")
    if defender.stats["health"] == 0:
        defender.disconnected = True
        print(f"{defender.name.title()} disconnected!")