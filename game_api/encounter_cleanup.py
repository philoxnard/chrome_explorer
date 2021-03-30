


def encounter_cleanup(self):
    print('encounter is over')
    for phox in self.player.party:
        phox.can_act = False
        phox.is_attacking = False
        phox.RAM = phox.max_RAM
    print("Returning to explore state")
    add_to_collection(self.wild_phox.species, self.player, self.players)
    self.state = "explore"

def add_to_collection(phox_name, player, playerDB):
    collection = get_collection(player, playerDB)
    check_if_in_collection(phox_name, collection, player, playerDB)

def get_collection(player, playerDB):
    player_db_info = playerDB.find({"username": player.username})
    for doc in player_db_info:
        collection = doc["collection"]
        return collection

def check_if_in_collection(phox_name, collection, player, playerDB):
    name_list = []
    for key in collection:
        name_list.append(key)
    if phox_name in name_list:
        print(f"You already have a {phox_name}")
    else:
        print(f"Adding {phox_name} to your collection.")
        nickname = get_nickname()
        add_phox(phox_name, playerDB, player, nickname)

def get_nickname():
    nickname = input("What do you want to name it?")
    return nickname

def add_phox(phox_name, playerDB, player, nickname):
    phox_dict = {}
    phox_dict["experience"] = 0
    phox_dict["level"] = 1
    phox_dict["upgrade indexes"] = []
    phox_dict["nickname"] = nickname
    phox_dict["in_party"] = False
    species_string = "collection." + phox_name
    playerDB.update({"username": player.username}, 
    {"$set":{
        species_string: phox_dict,
    }})