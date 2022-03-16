"""
Helper functions for app.py
"""

from flask import Flask, request, json, Response, render_template, session, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, send
import logging


from game import Game

__logger = logging.getLogger(__name__)
__logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(message)s')
handler.setFormatter(formatter)
__logger.addHandler(handler)

app = Flask(__name__)
CORS(app)
app.secret_key = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, cors_allowed_origins="*")

def getGameSession(games, sid=None):
    """
    Top level function for handling a new connection. We take the following steps:

    1) Get the user's IP address
    2) Check to see if a session with that IP address already exists
    3) If not, we create a new game session with that IP address
    4) It then returns the state of the game in question
    """

    ip = getPlayerIPAddress()

    result = doesGameSessionAlreadyExist(ip, games)
    if result == False:
        game = createGameSession(sid, ip, games)
    else:
        game = getGame(ip, games)

    return game

def getPlayerIPAddress():

    ip = request.remote_addr
    print("Found connection is ip address " + str(ip))
    return ip

def doesGameSessionAlreadyExist(ip, games):
    """
    This function takes the IP address of the connecting computer and uses it to check if we already
    have a game session using that IP address.
    """

    if not any(game.ip == ip for game in games):
        print("Game with ip address does not currently exist")
        return False

    else:
        print("Game with ip address already exists")
        return True


def createGameSession(sid, ip, games):
    """
    This function adds a game to the list of currently active game sessions.

    """
    game = Game(ip)
    games.append(Game(ip))

    game.state = "initialize"
    return game

def getGame(ip, games):
    """
    This function gets called if the current IP address has an existing game associated with it.

    It returns that game instance.
    """
    print('inside get game')
    for game in games:
        if game.ip == ip:
           return game

def handleUpgradeSelect(game, phox, row, option):

    success = game.select_upgrade(phox, int(row), int(option))
    if success:
        game.reload_needed = True
        return phox

def getPhoxInParty(game, phox_species):

    for phox in game.player.party:

        if phox.species.title() == phox_species and game.at_phoxtrot:
            return phox

def getPlayerSelectedAttack(attack_name, phox, game):
    game.player_attack = attack_name.lower()
    for attack in phox.attacks:
        if attack.name == game.player_attack:
            return attack

def reloadGame(game):

    if game.reload_needed:
        playerinfo = game.players.find({"username": game.player.username})
        game.player.party = []
        game.instantiate_party()
        game.reload_needed = False

def resetPhoxUpgrade(game, phox):

    # We need to create a string out that's formatted such that the database will accept it
    db_friendly_string = "collection." + phox.species + ".upgrade indexes"

    # Write to the database with the new upgrade indexes
    game.players.update_one({"username": game.player.username},
    {"$set":{db_friendly_string: []}})
