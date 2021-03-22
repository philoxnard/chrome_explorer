import player
import monster

import os
from dotenv import load_dotenv
import pymongo

load_dotenv()
mongo_URI = os.getenv("mongo_URI")
client = pymongo.MongoClient(mongo_URI)
db = client.my_database
regions = db.regions

class Game:
    """
    A class to model a game session
    """

    def __init__(self):

        self.region_dict = self.get_region_dict()
        self.player = self.add_player()
        self.encounter_frequency = 100
        self.region = None
        self.regions = regions
        self.phox_encountered = None

    from game_api.url_handler import handle_new_url
    from game_api.determine_encounter import determine_encounter

    # Skeleton function to instantiate the player when the game starts.
    def add_player(self):
        return player.Player()

    # Runs when a game session is instantiated to grab the potential regions from the DB
    def get_region_dict(self):
        regions_dict = {}
        for doc in regions.find():
            region = doc["region"]
            domains = doc["domains"]
            regions_dict[region] = domains
        return regions_dict

game = Game()
game.add_player()
game.handle_new_url()