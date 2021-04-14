from game_api.instantiate_party import  combine_phox_stats

############################################################################
### Library for giving a phox experience, leveling it up, and storing it ###
############################################################################



def handle_experience(self, phox, enemy, player, playerDB):
    self.cleanup_info_dict["phox"] = phox.name.title()
    exp_constant = 2
    if phox.level < self.level_cap:
        exp_gained = round(enemy.level*exp_constant*phox.exp_mod)
        phox.experience += int(exp_gained)
        print(f"{phox.name.title()} gained {exp_gained} experience.")
        self.cleanup_info_dict["experience"] = exp_gained
        level = check_level(phox, player, playerDB)
        store_phox_in_db(phox, player, playerDB)
        if level:
            self.cleanup_info_dict["level"] = level
    else:
        self.cleanup_info_dict["experience"] = 0

def check_level(phox, player, playerDB):
    level = round(phox.experience**(1/3))
    if not phox.level == level:
        level_up(phox, level, player, playerDB)
        return level
        
def level_up(phox, level, player, playerDB):
    phox.level = level
    print(f"{phox.name.title()} grew to level {level}!")
    combine_phox_stats(phox)
    

def store_phox_in_db(phox, player, playerDB):
    exp_string = "collection." + phox.species + ".experience"
    lvl_string = "collection." + phox.species + ".level"
    playerDB.update({"username": player.username}, 
    {"$set":{
    exp_string: phox.experience,
    lvl_string: phox.level}})