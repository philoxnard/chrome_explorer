global_mod = 3

#################################################################
### Library for dealing with an attack and calculating damage ###
#################################################################

def execute_attack(attacker, defender, attack):
    print(f"{attacker.name.title()} is attacking {defender.name.title()} with {attack.name.title()}")
    attacker.RAM -= attack.cost
    print(f"{attacker.name.title()} spent {attack.cost} RAM and now has {attacker.RAM}")
    damage = int(calculate_damage(attacker, defender, attack))
    print(f"The attack dealt {damage} damage")

def calculate_damage(attacker, defender, attack):
    lvl_mod = get_lvl_mod(attacker, defender, attack)
    attacker_stat = get_attacker_stat(attacker, defender, attack)
    defender_stat = get_defender_stat(attacker, defender, attack)
    other = get_other_mod(attacker, defender, attack)
    print(f"Formula: {lvl_mod}*{attacker_stat}/{defender_stat}*{other}")
    damage = lvl_mod*attack.damage*attacker_stat/defender_stat*other/global_mod
    return damage

def get_lvl_mod(attacker, defender, attack):
    mod = attacker.level - defender.level
    if mod > 0:
        mod = 1 + float(mod/10)
    elif mod < 0:
        mod = 1 - float(mod/10)
    elif mod == 0:
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
        defender_ = 1
    return defender_stat

def get_other_mod(attacker, defender, attack):
    family_mod = get_family_mod(attacker, defender, attack)
    print(f"family mod is {family_mod}")
    STAB = get_STAB(attacker, attack)
    print(f"STAB is {STAB}")
    mod = float(STAB*family_mod)
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

