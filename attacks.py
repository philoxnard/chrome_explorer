

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
                for clash_title, clash_effect in effect[2].items():
                    if clash_title == "cpow_mod":
                        attacker.temp_cpow *= clash_effect
                        pre_effect_dict["pre effect"]+=(f"CPOW multipled by {clash_effect}! ")

                    elif clash_title == "lpow_mod":
                        pre_effect_dict["pre effect"]+=(f"LPOW multipled by {clash_effect}! ")
                        attacker.temp_lpow *= clash_effect

                pre_effect_dict["clash"] = "You passed the clash!"
            else:
                pre_effect_dict["clash"] = "You failed the clash!"

        # Code for handling non clash effects


    return pre_effect_dict



def post_attack_effect(attacker, defender, attack):
    post_effect_dict = {"post effect": ""}
    for title, effect in attack.effect.items():

        if title == "as_boost":
                attacker.AS += effect
                post_effect_dict["post effect"]= f"Gained 20 {effect} AS!"

    return post_effect_dict
    
def determine_clash(attacker, defender, effect):
    attacker_stat = effect[0]
    defender_stat = effect[1]
    print(attacker.stats[attacker_stat])
    print(defender.stats[defender_stat])
    if attacker.stats[attacker_stat] > defender.stats[defender_stat]:
        return True