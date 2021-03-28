from game_api.instantiate_party import  combine_phox_stats

############################################################################
### Library for giving a phox experience, leveling it up, and storing it ###
############################################################################



def handle_experience(self, phox, enemy, player, playerDB):
    exp_constant = 2
    exp_gained = enemy.level*exp_constant*phox.exp_mod
    phox.experience += exp_gained
    print(f"{phox.name.title()} gained {exp_gained} experience.")
    check_level(phox, player, playerDB)

def check_level(phox, player, playerDB):
    level = round(phox.experience**(1/3))
    if not phox.level == level:
        level_up(phox, level, player, playerDB)
        
def level_up(phox, level, player, playerDB):
    phox.level = level
    print(f"{phox.name.title()} grew to level {level}!")
    combine_phox_stats(phox)
    store_phox_in_db(phox, player, playerDB)

def store_phox_in_db(phox, player, playerDB):
    playerDB.update_one({"username": player.username}, {
        "$set": {
            "collection":{
                phox.species:{
                    "experience": phox.experience,
                    "level": phox.level
                }
            }
        }
    })
