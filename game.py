import os
from dotenv import load_dotenv
import pymongo
import json

load_dotenv()
# In the future, I'll need to put this mongo_URI into a dotenv file.
mongo_URI = "mongodb+srv://userphil:o8puwmVASyTiebHB@cluster0.hmrog.mongodb.net/my_database?retryWrites=true&w=majority"
client = pymongo.MongoClient(mongo_URI)
db = client.my_database

class Game:
    """
    A class to model a game session
    """

    def __init__(self, ip):
        print('initializing')
        # Used to keep games seperate between users
        self.ip = ip

        # Game state! Very important
        self.state = "initialize"

        # On initialization, we grab all of the information from the database and store
        # them into variables here. Might be too work intensive, could possibly improve
        # in the future
        self.regions = db.regions
        self.players = db.players
        self.phoxes = db.phoxes
        self.attacks = db.attacks
        self.upgrades = db.upgrades
        self.families = db.families

        # Login assist
        self.username = None
        self.password = None
        self.secret_key = os.getenv("secret_key")

        # The instance of a wild phox that appears while exploring
        self.wild_phox = None

        # Attributes that determine themselves by connecting to the database
        self.region_dict = self.get_region_dict()
        self.player = None

        # Percentage odds of having an encounter while trotting
        self.encounter_frequency = 100

        # String taken from the handle_new_url library
        self.region = None

        # String taken from the determine_encounter library
        self.phox_encountered = None

        # Helps display the proper info in combat
        self.combat_state = None
        self.player_attack = None

        # Pushed to client to display information in the combat readout
        self.combat_info_dict = {}

        # Dictionary pushed to client after combat to display experience gain and
        # possible new phox addition
        self.cleanup_info_dict = {}

        # The max level for phoxes. If the game goes live, this may be increased
        self.level_cap = 20

        # Set to true whenever a phox gets a change to its upgrade so that the game
        # knows to reinstantiate it when the popup closes
        self.reload_needed = False

        # Used to determine whether or not the player is currently at phoxtrot.com
        self.at_phoxtrot = False

    # Import the high level functions from the different API libraries
    from game_api.handle_login import handle_login, terminal_test_login
    from game_api.handle_new_url import new_url_handler
    from game_api.determine_encounter import determine_encounter
    from game_api.instantiate_party import instantiate_party
    from game_api.initialize_encounter import initialize_encounter
    from game_api.combat import combat, execute_player_attack, check_disconnect_and_shutdown
    from game_api.experience import handle_experience
    from game_api.encounter_cleanup import encounter_cleanup
    from game_api.handle_phoxtrot_site import handle_phoxtrot_site, get_collection_data
    from game_api.handle_upgrades import select_upgrade
    from game_api.handle_collection_swap import swap_collection

    def get_state(self):
        return self.state

    def getPlayerActivePhox(self):
        for phox in self.active_phoxes:
            if phox.is_wild == False:
                return phox

    def getPlayerCollection(self):
        """
        This function returns the names of all of the phoxes that the user has in their collection
        """

        collection = []

        player_in_DB = game.players.find({"username": game.player.username})
        for doc in player_in_DB:
            for phox in doc["collection"]:
                collection.append(phox.title())

        return collection

    # Runs when a game session is instantiated to grab the potential regions from the DB
    def get_region_dict(self):
        regions_dict = {}
        print(self.regions)
        for doc in self.regions.find():
            region = doc["region"]
            domains = doc["domains"]
            regions_dict[region] = domains
        return regions_dict

    def get_info_dict(self):
        info_dict = {}
        info_dict["wild_phox_max_hp"]=self.wild_phox.max_health
        info_dict["wild_phox_current_hp"]=self.wild_phox.stats["health"]
        info_dict["wild_phox_max_RAM"]=self.wild_phox.max_RAM
        info_dict["wild_phox_current_RAM"]=self.wild_phox.RAM
        info_dict["wild_phox_name"]=self.wild_phox.name.title()
        info_dict["wild_phox_level"]=self.wild_phox.level
        info_dict["wild_phox_status"]=self.wild_phox.status
        info_dict["wild_phox_art"]=self.wild_phox.enemy_art
        for phox in self.active_phoxes:
            if not phox.is_wild:
                    info_dict["phox_max_hp"]=phox.max_health
                    info_dict["phox_current_hp"]=phox.stats["health"]
                    info_dict["phox_max_RAM"]=phox.max_RAM
                    info_dict["phox_current_RAM"]=phox.RAM
                    info_dict["phox_name"]=phox.name.title()
                    info_dict["phox_level"]=phox.level
                    info_dict["phox_status"]=phox.status
                    info_dict["phox_art"]=phox.player_art
        return info_dict

    def refresh_player(self):
        print('firing')
        self.players = db.players

    def swapActivePhox(self, old_phox, new_phox):

        new_phox.enterCombat()
        # there should probably be a function here that's like, old_phox.leaveCombat()
        self.active_phoxes.remove(old_phox)
        self.active_phoxes.insert(0, new_phox)
        self.combat_state = None

if __name__ == '__main__':
    game = Game("localhost")