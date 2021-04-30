

##################################################
### Library for generating effects for talents ###
##################################################

# Library called by intantiate_party.py

# Takes info from each attack dictionary and applies an actual effect
# based on the effect of the attack.

# This way, attacks can be updated by changing them in the database.
# However, this document must be updated each time an attack is made with 
# a brand new effect.

# NOTE: This will probably only actually ever get called in battle
# This doc will get updated when combat is further in development


def pre_attack_effect(attacker, defender, attack):
    pre_effect_dict = {"pre effect": ""}
    for title, effect in attack.effect.items():

        # Code for handling clashes and their effects
        if title == "clash":
            clash = determine_clash(attacker, defender, effect)
            if clash:
                
                # Code for handling successful clashes
                for clash_title, clash_effect in effect[2].items():

                    if clash_title == "cpow_mod":
                        attacker.temp_cpow *= clash_effect
                        pre_effect_dict["pre effect"]+=(f"CPOW multipled by {clash_effect}! ")
                        if defender.copypaste:
                            defender.temp_cpow *= clash_effect
                            pre_effect_dict["pre effect"]+=(f"{defender.name.title()} copied the stat boost! ")

                    if clash_title == "lpow_mod":
                        pre_effect_dict["pre effect"]+=(f"LPOW multipled by {clash_effect}! ")
                        attacker.temp_lpow *= clash_effect
                        if defender.copypaste:
                            defender.temp_lpow *= clash_effect
                            pre_effect_dict["pre effect"]+=(f"{defender.name.title()} copied the stat boost! ")

                    if clash_title == "damage_mod":
                        pre_effect_dict["pre effect"]+=(f"Damage multipled by {clash_effect}! ")
                        attacker.temp_damage_mod *= clash_effect

                pre_effect_dict["clash"] = "Clash success!"
            else:

                # Code for handling unsuccessful clashes
                if len(effect)>3:
                    for clash_title, clash_effect in effect[3].items():

                        if clash_title == "vis_mod":
                            pre_effect_dict["pre effect"]+=(f"VIS multipled by {clash_effect}! ")
                            attacker.temp_vis *= clash_effect
                            if defender.copypaste:
                                defender.temp_vis *= clash_effect
                                pre_effect_dict["pre effect"]+=(f"{defender.name.title()} copied the stat boost! ")

                pre_effect_dict["clash"] = "Clash failed..."

        # Code for handling non clash effects
        # Stat boosts
        if title == "csec_mod":
            attacker.temp_csec *= effect
            pre_effect_dict["pre effect"]+=(f"CSEC multipled by {effect}! ")
            if defender.copypaste:
                defender.temp_csec *= effect
                pre_effect_dict["pre effect"]+=(f"{defender.name.title()} copied the stat boost! ")

        if title == "lsec_mod":
            attacker.temp_lsec *= effect
            pre_effect_dict["pre effect"]+=(f"LSEC multipled by {effect}! ")
            if defender.copypaste:
                defender.temp_lsec *= effect
                pre_effect_dict["pre effect"]+=(f"{defender.name.title()} copied the stat boost! ")
        
        if title == "cpow_mod":
            attacker.temp_cpow *= effect
            pre_effect_dict["pre effect"]+=(f"CPOW multipled by {effect}! ")
            if defender.copypaste:
                defender.temp_cpow *= effect
                pre_effect_dict["pre effect"]+=(f"{defender.name.title()} copied the stat boost! ")
        
        if title == "lpow_mod":
            attacker.temp_lpow *= effect
            pre_effect_dict["pre effect"]+=(f"LPOW multipled by {effect}! ")
            if defender.copypaste:
                defender.temp_lpow *= effect
                pre_effect_dict["pre effect"]+=(f"{defender.name.title()} copied the stat boost! ")

        # Stat drains
        if title == "csec_drain":
            defender.temp_csec *= effect
            pre_effect_dict["pre effect"]+=(f"Defender CSEC multipled by {effect}! ")
        
        if title == "lsec_drain":
            defender.temp_lsec *= effect
            pre_effect_dict["pre effect"]+=(f"Defender LSEC multipled by {effect}! ")

        if title == "lpow_drain":
            defender.temp_lpow *= effect
            pre_effect_dict["pre effect"]+=(f"Defender LPOW multipled by {effect}! ")

        if title == "cpow_drain":
            defender.temp_cpow *= effect
            pre_effect_dict["pre effect"]+=(f"Defender CPOW multipled by {effect}! ")

        if title == "speed_drain":
            defender.temp_csec *= effect
            pre_effect_dict["pre effect"]+=(f"Defender SPEED multipled by {effect}! ")

        # Other
        if title == "first_attack":
            if attacker.first_attack:
                pre_effect_dict["pre effect"]+=(f"{attacker.name.title()} made the first post! ")
                attack.damage = effect
            elif not attacker.first_attack:
                pre_effect_dict["pre effect"]+=(f"Too late... ")
                attack.damage = 0

        if title == "repost_ramp":
            pre_effect_dict["pre effect"]+=(f"{attack.name.title()} damage multiplied by {effect}! ")
            attacker.repost_mod *= effect

        if title == "turn_ramp":
            attacker.PoW_mod = effect*(attacker.turns_active+defender.turns_active)

        if title == "status":
            if not effect in defender.status and not effect in defender.immunities:
                defender.status.append(effect)
                pre_effect_dict["pre effect"]+=(f"{defender.name.title()} afflicted by {effect}! ")
            elif effect in defender.immunities:
                pre_effect_dict["pre effect"]+=(f"{defender.name.title()} is immune to {effect}! ")
            elif effect in defender.status:
                pre_effect_dict["pre effect"]+=(f"{defender.name.title()} was already afflicted by {effect}! ")

    return pre_effect_dict



def post_attack_effect(attacker, defender, attack):
    post_effect_dict = {"post effect": ""}
    for title, effect in attack.effect.items():

        if title == "as_boost":
                attacker.AS += effect
                post_effect_dict["post effect"]+=(f"Gained {effect} AS!")

    if defender.regenerate > 0:
        health_gain = int(defender.regenerate * defender.max_health)
        defender.stats["health"]+=health_gain
        if defender.stats["health"] > defender.max_health:
            defender.stats["health"] = defender.max_health
        post_effect_dict["post effect"]+=(f'{defender.name.title()} restored {health_gain} health!')

    return post_effect_dict
    
def determine_clash(attacker, defender, effect):
    attacker_stat = effect[0]
    defender_stat = effect[1]
    print(attacker.stats[attacker_stat])
    print(defender.stats[defender_stat])
    if attacker.stats[attacker_stat] > defender.stats[defender_stat]:
        return True

# def check_copy_paste_pre(defender, pre_effect_dict, temp_stat, stat_mod):
#     if defender.copypaste == True:
#         defender.temp_stat *= stat_mod
#         pre_effect_dict["pre effect"]+=(f"Opponent copied the stat boost! ")
#     return pre_effect_dict