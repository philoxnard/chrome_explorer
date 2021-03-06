from flask import Flask, request, json, Response, render_template, session, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, send
import logging

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
    __logger.info("new connection")
    ip = "100.0.28.103" # request.remote_addr
    if not any(game.ip == ip for game in games):
        games.append(Game(ip))
        __logger.info(f"Creating new game with IP {ip}")
        state = "initialize"
        socketio.emit('update state', state, room=sid)
    else:
        __logger.info(f"Game already exists with IP {ip}")  
        for game in games:
            if game.ip == ip:
                state = game.state
                __logger.info(f"Current state is {state}")
                socketio.emit('update state', state, room=sid)
                if game.combat_info_dict:
                    readout = game.combat_info_dict
                    socketio.emit('update readout', readout, room=sid)
                elif game.combat_state == "waiting":
                    socketio.emit('your turn readout', room=sid)
                if game.reload_needed:
                    playerinfo = game.players.find({"username": game.player.username})
                    game.player.party = []
                    game.instantiate_party()
                    game.reload_needed = False


@socketio.on('login')
def handle_login(sid, username, password, methods=['GET', "POST"]):
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            game.username = username
            game.password = password
            game.handle_login()
            if game.state == "idle":
                __logger.info('login successful')
                state = game.state
                socketio.emit('update state', state, room=sid)
            else:
                __logger.info('login not successful')

@app.route('/newUrl', methods=["POST"])
def handle_test():
    ip = "100.0.28.103" # request.remote_addr
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

@app.route('/exit', methods=["GET"])
def handle_exit():
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            games.remove(game)
            __logger.info(games)
            __logger.info('found exit')
            return 'success', 200
    return 'no exit', 200

@socketio.on('start trotting')
def start_trotting(methods=["GET"]):
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            game.cleanup_info_dict = {}
            game.state = "explore"
            __logger.info(f"The current state is {game.state}")

@socketio.on('stop trotting')
def stop_trotting(methods=["GET"]):
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            game.state = "idle"
            __logger.info(f"The current state is {game.state}")

@socketio.on('combat loop')
def handle_combat_loop(sid, methods=["GET"]):
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            game.state = "encounter"
            game.combat()
            socketio.emit('update state', game.state, room=sid)
            if not game.combat_state == "waiting":
                readout = game.combat_info_dict
                socketio.emit('update readout', readout, room=sid)
                if game.active_phoxes[0].disconnected:
                    game.check_disconnect_and_shutdown()
                    # if game.player.shutdown:
                    #     socketio.emit('update state', game.state, room=sid)

            else:
                socketio.emit('your turn readout', room=sid)
            if game.state == "encounter cleanup":
                game.encounter_cleanup()
                

@socketio.on('initialize encounter state')
def start_combat(sid, methods=["GET"]):
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            info_dict = game.get_info_dict()
            socketio.emit('draw details', info_dict, room=sid)

@socketio.on('get attack menu')
def get_attack_menu(sid, methods=["GET"]):
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            for phox in game.active_phoxes:
                if not phox.is_wild:
                    json_list = []
                    for attack in phox.attacks:
                        json_list.append(attack.serialize())
                    socketio.emit('generate attack menu', json_list, room=sid)                      

@socketio.on('click attack')
def handle_attack_click(attack_name, sid, methods=["GET"]):
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            if game.combat_state == "waiting":
                print('found')
                __logger.info(attack_name)
                if not game.active_phoxes[0].disconnected:
                    game.player_attack = attack_name.lower()
                    for attack in game.active_phoxes[0].attacks:
                        if attack.name == game.player_attack:
                            if game.active_phoxes[0].RAM >= attack.cost:
                                game.execute_player_attack()
                                info_dict = game.get_info_dict()
                                socketio.emit('draw details', info_dict, room=sid)
                                readout = game.combat_info_dict
                                socketio.emit('update readout', readout, room=sid)
                            else:
                                socketio.emit('not enough RAM', room=sid)
                else:
                    print('the phox is disconnected ')

@socketio.on('get cleanup info')
def handle_combat_cleanup(sid, methods=["GET"]):
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            if game.state == "encounter cleanup":
                info_dict = game.cleanup_info_dict
                socketio.emit('display cleanup', info_dict, room=sid)

@socketio.on('view party')
def handle_party_view(sid, methods=["GET"]):
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            json_list = []
            for phox in game.player.party:
                json_attacks = []
                json_upgrades = []
                json_base_upgrades = []
                for attack in phox.attacks:
                    json_attacks.append(attack.serialize())
                for index, row in enumerate(phox.upgrade_tree):
                    json_upgrades.append([])
                    for upgrade in row:
                        json_upgrades[index].append(upgrade.serialize())
                for upgrade in phox.base_upgrades:
                    json_base_upgrades.append(upgrade.serialize())
                json_phox = phox.serialize()
                json_phox["base upgrades"]= json_base_upgrades
                json_phox["upgrade tree"] = json_upgrades
                json_phox["attacks"] = json_attacks
                json_list.append(json_phox)
            socketio.emit('draw party', json_list, room=sid)
            if game.at_phoxtrot:
                collection = []
                player = game.players.find({"username": game.player.username})
                for doc in player:
                    for phox in doc["collection"]:
                        collection.append(phox.title())
                    __logger.info(collection)
                socketio.emit('draw collection', collection, room=sid)

@socketio.on('select phox')
def handle_select_phox(raw_phox, sid, methods=["GET"]):
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
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
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            for phox in game.player.party:
                if phox.species.title() == phox_species.title() and game.at_phoxtrot:
                    phox.upgrade_indexes = []
                    db_friendly_string = "collection." + phox.species + ".upgrade indexes"
                    game.players.update_one({"username": game.player.username}, 
                    {"$set":{db_friendly_string: []}})
                    socketio.emit('display reset upgrades', room=sid)
                    game.reload_needed = True

@socketio.on('select upgrade')
def handle_upgrade_select(phox_species, row, option, sid, methods=["GET"]):
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            for phox in game.player.party:
                if phox.species.title() == phox_species and game.at_phoxtrot:
                    success = game.select_upgrade(phox, int(row), int(option))
                    if success:
                        socketio.emit('update upgrades', phox.upgrade_indexes, room=sid)
                        game.reload_needed = True

@socketio.on('swap collection')
def handle_collection_swap(phox_species, sid, methods=["GET"]):
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            game.swap_collection(phox_species.lower())
            socketio.emit('callback view party', room=sid)


if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True)