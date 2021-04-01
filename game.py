import os
from dotenv import load_dotenv
import pymongo

load_dotenv()
mongo_URI = os.getenv("mongo_URI")
client = pymongo.MongoClient(mongo_URI)
db = client.my_database

class Game:
    """
    A class to model a game session
    """

    def __init__(self):

        # Game state! Very important
        self.state = "initialize"

        # Get all the info from the databases
        # This may get tweaked or removed, might be really work heavy
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

    # Import the high level functions from the different API libraries
    from game_api.handle_login import handle_login
    from game_api.handle_new_url import new_url_handler
    from game_api.determine_encounter import determine_encounter
    from game_api.instantiate_party import instantiate_party
    from game_api.initialize_encounter import initialize_encounter
    from game_api.combat import combat
    from game_api.experience import handle_experience
    from game_api.encounter_cleanup import encounter_cleanup
    from game_api.handle_phoxtrot_site import handle_phoxtrot_site
    

    # Runs when a game session is instantiated to grab the potential regions from the DB
    def get_region_dict(self):
        regions_dict = {}
        for doc in self.regions.find():
            region = doc["region"]
            domains = doc["domains"]
            regions_dict[region] = domains
        return regions_dict