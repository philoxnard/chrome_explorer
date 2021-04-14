


def encounter_cleanup(self):
    print('encounter is over')
    for phox in self.player.party:
        phox.can_act = False
        phox.is_attacking = False
        phox.RAM = phox.max_RAM
    new_phox = add_to_collection(self.wild_phox.species, self.player, self.players)
    if new_phox:
        self.cleanup_info_dict["newPhox"] = new_phox.title()

def add_to_collection(phox_name, player, playerDB):
    collection = get_collection(player, playerDB)
    new_phox = check_if_in_collection(phox_name, collection, player, playerDB)
    return new_phox

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
        nickname = "sample nickname" # to be changed when integrated with front end
        add_phox(phox_name, playerDB, player, nickname)
        return phox_name

# Eventually gonna need to make it so that, if your party isn't full, the new phox
# goes into your party instead of your collection
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