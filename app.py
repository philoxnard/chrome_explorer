from flask import Flask, request, json, Response, render_template, session, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, send
import logging

from app_helper import *
from game import Game
games = []

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

@socketio.on('connection')
def handle_new_connection(sid, methods=['GET', "POST"]):
    """
    This function gets called whenever a user opens up the Phoxtrot chrome extention.

    First, we grab the ip address of the computer attempting to access the game.
        Note that this should change in the future because IP address is a bad way to do it -
        potentially limits how people can actually play the game. We need a way to differentiate
        users, but this probably isn't the right way.

    Then, we check to see if a game with that IP exists. If not, we create it. If yes, we emit
    that game's state to the front end.

    Lastly, if we're in combat, we'll need to get a specific readout for where we are in combat
    """
    __logger.info("new connection")

    game = getGameSession(games, sid)
    socketio.emit('update state', game.state, room=sid)

    # If we're currently in combat, we need to get the appropriate readout to be displayed to 
    # the user
    if game.combat_info_dict:
        readout = game.combat_info_dict
        socketio.emit('update readout', readout, room=sid)
    elif game.combat_state == "waiting":
        socketio.emit('your turn readout', room=sid)

    # If the user has recently changed their party somehow, we need to re-instantiate their party.
    reloadGame(game)



@socketio.on('login')
def handle_login(sid, username, password, methods=['GET', "POST"]):

    game = getGameSession(games, sid)
    game.username = username
    game.password = password
    game.handle_login()
    state = game.get_state()
    if state == "idle":

        __logger.info('login successful')
        socketio.emit('update state', state, room=sid)
    else:

        __logger.info('login not successful')

# idk what this is for?##################################3
@app.route('/newUrl', methods=["POST"])
def handle_test():
    ip = request.remote_addr # request.remote_addr
    for game in games:
        if game.ip == ip:
            if game.state == "explore" or game.state == "idle":
                if game.reload_needed:
                    playerinfo = game.players.find({"username": game.player.username})
                    game.player.party = []
                    game.instantiate_party()
                    game.reload_needed = False
                raw_url = request.get_data()
                url = str(raw_url, 'UTF-8')
                game.player.url = url
                game.new_url_handler()
            elif game.state == "idle":
                __logger.info("Start trotting to find a phox!")
            return jsonify({"state": game.state}), 200
    return jsonify('none'), 200
############################################################

@app.route('/exit', methods=["GET"])
def handle_exit():

    game = getGameSession(games)
    games.remove(game)
    __logger.info(games)
    __logger.info('found exit')
    return 'success', 200

@socketio.on('start trotting')
def start_trotting(methods=["GET"]):

    game = getGameSession(games)
    game.cleanup_info_dict = {}
    game.state = "explore"
    __logger.info(f"The current state is {game.state}")

@socketio.on('stop trotting')
def stop_trotting(methods=["GET"]):

    game = getGameSession(games)
    game.state = "idle"
    __logger.info(f"The current state is {game.state}")

@socketio.on('combat loop')
def handle_combat_loop(sid, methods=["GET"]):
    """
    This function is called either when a new encounter is accepted, or when it becomes
    the player clicks "next turn".
    """
    game = getGameSession(games)
    game.state = "encounter"
    game.combat()
    socketio.emit('update state', game.state, room=sid)
    if not game.combat_state == "waiting":
        readout = game.combat_info_dict
        socketio.emit('update readout', readout, room=sid)

    else:
        socketio.emit('your turn readout', room=sid)
    if game.state == "encounter cleanup":
        game.encounter_cleanup()


@socketio.on('initialize encounter state')
def start_combat(sid, methods=["GET"]):

    game = getGameSession(games)
    info_dict = game.get_info_dict()
    socketio.emit('draw details', info_dict, room=sid)

@socketio.on('get attack menu')
def get_attack_menu(sid, methods=["GET"]):

    game = getGameSession(games)
    phox = game.getActivePlayerPhox()
    json_list = phox.getAttacksAsJSON()
    socketio.emit('generate attack menu', json_list, room=sid)

@socketio.on('click attack')
def handle_attack_click(attack_name, sid, methods=["GET"]):

    __logger.info(attack_name)

    game = getGameSession(games)
    if game.combat_state == "waiting":

        # This means that the game is waiting for the player to take their turn.
        # Nothing will happen until the user executes an attack

        # This is probably a bad way to do it, but this check exists to ensure that
        # combat continues while the player phox has disconnected. Their options at
        # this point are to swap or to run
        phox = game.getPlayerActivePhox()
        if phox.disconnected == False:

            # This function uses the attack_name to get the actual attack object from the active phox
            attack = getPlayerSelectedAttack(attack_name, phox, game)
            success = phox.doesPhoxHaveEnoughRAM(attack)
            if success == True:

                game.execute_player_attack()

                info_dict = game.get_info_dict()
                readout = game.combat_info_dict

                socketio.emit('draw details', info_dict, room=sid)
                socketio.emit('update readout', readout, room=sid)
            else:
                socketio.emit('not enough RAM', room=sid)
        else:
            print('the phox is disconnected ')

@socketio.on('get cleanup info')
def handle_combat_cleanup(sid, methods=["GET"]):
    game = getGameSession(games)
    if game.state == "encounter cleanup":
        info_dict = game.cleanup_info_dict
        socketio.emit('display cleanup', info_dict, room=sid)

@socketio.on('view party')
def handle_party_view(sid, methods=["GET"]):

    game = getGameSession()

    # We need to put all of the information for each phox in a list, then send that list
    # to the front end so that it can be displayed
    json_list = []
    for phox in game.player.party:
        json_phox = phox.getFullJSONPhox()
        json_list.append(json_phox)

    socketio.emit('draw party', json_list, room=sid)

    # If the user is at phoxtrot.com, we also need to display a list of all of the Phoxes
    # in their PC
    if game.at_phoxtrot:

        # Get the player object from the database
        collection = game.getPlayerCollection()

        socketio.emit('draw collection', collection, room=sid)

@socketio.on('select phox')
def handle_select_phox(raw_phox, sid, methods=["GET"]):

    game = getGameSession(games)
    selected_phox = raw_phox.partition("<")[0].lower()
    __logger.info(selected_phox)
    for phox in game.player.party:
        if phox.species == selected_phox:
            __logger.info("found the selected phox")
            __logger.info(game.state)
            __logger.info(game.combat_state)
            if phox.disconnected:
                __logger.info("disconnected")
            if game.state == "encounter" and game.combat_state == "waiting":
                __logger.info("game state is correct")
                if not phox.disconnected:
                    __logger.info("the selected phox is not disconnected")
                    for active_phox in game.active_phoxes:
                        if not active_phox.is_wild:
                            # function to reset phox's AS and temp stats
                            active_phox.first_attack = True
                            game.active_phoxes.remove(active_phox)
                            game.active_phoxes.insert(0, phox)
                            __logger.info(f'Swapping out {active_phox.name} for {phox.name}')
                            active_phox.can_act = False
                            game.combat_state = None
                            socketio.emit('swapped phox', phox.name, room=sid)
                            __logger.info(f'swapping to {phox.name}')
            elif game.state == "idle" or game.state == "explore":
                socketio.emit('view phox', selected_phox.title(), room=sid)

@socketio.on('reset upgrades')
def handle_upgrade_reset(phox_species, sid, methods=["GET"]):

    game = getGameSession(games)
    phox = getPhoxInParty(game, phox_species)
    phox.resetUpgradeIndexes()
    resetPhoxUpgrade(game, phox)

    socketio.emit('display reset upgrades', room=sid)
    game.reload_needed = True

@socketio.on('select upgrade')
def handle_upgrade_select(phox_species, row, option, sid, methods=["GET"]):

    game = getGameSession(games)
    phox = getPhoxInParty(game, phox_species)
    upgraded_phox = handleUpgradeSelect(game, phox, row, option)

    if upgraded_phox:
        socketio.emit('update upgrades', upgraded_phox.upgrade_indexes, room=sid)
        game.reload_needed = True

@socketio.on('swap collection')
def handle_collection_swap(phox_species, sid, methods=["GET"]):

    game = getGameSession(games)
    game.swap_collection(phox_species.lower())
    socketio.emit('callback view party', room=sid)


if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True)