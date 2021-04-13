from flask import Flask, request, json, Response, render_template, session, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, send

from game import Game
games = []

app = Flask(__name__)
CORS(app)
app.secret_key = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connection')
def handle_new_connection(sid, methods=['GET', "POST"]):
    print("new connection")
    ip = "100.0.28.103" # request.remote_addr
    if not any(game.ip == ip for game in games):
        games.append(Game(ip))
        print(f"Creating new game with IP {ip}")
        state = "initialize"
        socketio.emit('update state', state, room=sid)
    else:
        print(f"Game already exists with IP {ip}")  
        for game in games:
            if game.ip == ip:
                state = game.state
                print(f"Current state is {state}")
                socketio.emit('update state', state, room=sid)
                if game.combat_info_dict:
                    readout = game.combat_info_dict
                    socketio.emit('update readout', readout, room=sid)

@socketio.on('login')
def handle_login(sid, username, password, methods=['GET', "POST"]):
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            game.username = username
            game.password = password
            game.handle_login()
            if game.state == "idle":
                print('login successful')
                state = game.state
                socketio.emit('update state', state, room=sid)
            else:
                print('login not successful')

@app.route('/newUrl', methods={"POST"})
def handle_test():
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            if game.state == "explore":
                raw_url = request.get_data()
                url = str(raw_url, 'UTF-8')
                game.player.url = url
                game.new_url_handler()
            elif game.state == "idle":
                print("Start trotting to find a phox!")
    return jsonify({"state": game.state}), 200

@socketio.on('start trotting')
def start_trotting(methods=["GET"]):
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            game.cleanup_info_dict = {}
            game.state = "explore"
            print(f"The current state is {game.state}")

@socketio.on('stop trotting')
def stop_trotting(methods=["GET"]):
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            game.state = "idle"
            print(f"The current state is {game.state}")

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
                print(attack_name)
                game.player_attack = attack_name.lower()
                game.execute_player_attack()
                info_dict = game.get_info_dict()
                socketio.emit('draw details', info_dict, room=sid)
                readout = game.combat_info_dict
                socketio.emit('update readout', readout, room=sid)

@socketio.on('get cleanup info')
def handle_combat_cleanup(sid, methods=["GET"]):
    ip = "100.0.28.103" # request.remote_addr
    for game in games:
        if game.ip == ip:
            if game.state == "encounter cleanup":
                info_dict = game.cleanup_info_dict
                socketio.emit('display cleanup', info_dict, room=sid)

if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True)