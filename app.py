from flask import Flask, request, json, Response, render_template, session
from flask_cors import CORS
from flask_socketio import SocketIO, send
import json
import jsonpickle
from json import JSONEncoder


from game import Game
games = []

app = Flask(__name__)
app.secret_key = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connectx')
def handle_new_connection(ip, sid, methods=['GET', "POST"]):
    print("new connection")
    if not any(game.ip == ip for game in games):
        games.append(Game(ip))
        print(f"Creating new game with IP {ip}")
    else:
        print(f"Game already exists with IP {ip}")  
        for game in games:
            if game.ip == ip:
                state = game.state
                socketio.emit('update state', state, room=sid)

@socketio.on('login')
def handle_login(ip, sid, username, password, methods=['GET', "POST"]):
    for game in games:
        if game.ip == ip:
            game.username = username
            game.password = password
            print(sid)
            game.handle_login()
            if game.state == "idle":
                print('login successful')
                print('state is idle')
                socketio.emit('idle state', ip, room=sid)
            else:
                print('login not successful')

@socketio.on('test')
def handle_test(methods=["GET"]):
    print('found')

# @app.route('/start_trotting', methods=["GET"])
# def start_trotting():
#     session["game"].state = "explore"
#     print(f"The current state is {session['game'].state}")
#     return 'success', 200

# @app.route('/stop_trotting', methods=["GET"])
# def stop_trotting():
#     session["game"].state = "idle"
#     print(f"The current state is {session['game'].state}")
#     return 'success', 200

# @app.route('/logout', methods=["GET"])
# def handle_logout():
#     print('logout found')
#     session["game"].state = "initialize"
#     return 'success', 200

# @app.route('/send')
# def send_py_data():
#     return json.dumps("String")

if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True)