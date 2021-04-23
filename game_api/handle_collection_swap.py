

###########################################################################
### Library for swapping phoxes between a player's collection and party ###
###########################################################################

# General handler for swapping a phox out
def swap_collection(self, phox_species):
    pop_third_phox(self.player.party, self.player, self.players)
    increment_party_index(self.player.party, self.player, self.players)
    add_new_phox(phox_species, self.player, self.players)
    self.player.party = []
    self.instantiate_party()
        
    # if the party has 3 phoxes, pop the third phox
        # set that phox's 'in_party' to 10
    # in collection, if in_party is 0, make it 1
    # in collection, if in_party is 1, make it 2 (probably do these in reverse order)
    # take phox_species and set that phox's in_party to 0
    # self.instantiate_party()
    # redraw party

    pass

def pop_third_phox(party, player, playerDB):
    if len(party) == 3:
        third_phox = self.player.party[2]
        party.pop(2)
        in_party_string = "collection." + third_phox.species + ".in_party"
        playerDB.update({"username": player.username},
        {"$set":{
            in_party_string: 10
        }})

def increment_party_index(party, player, playerDB):
    for phox in party:
        in_party_string = "collection." + phox.species + ".in_party"
        playerDB.update({"username": player.username},
        {"$inc": {
            in_party_string: 1
        }})

def add_new_phox(phox_species, player, playerDB):
    in_party_string = "collection." + phox_species + ".in_party"
    playerDB.update({"username": player.username},
    {"$set": {
        in_party_string: 0
    }})