from flask import Flask, request, json, Response, render_template, session
from flask_cors import CORS
from flask_socketio import SocketIO, send

from game import Game
games = []

app = Flask(__name__)
app.secret_key = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connection')
def handle_new_connection(ip, sid, methods=['GET', "POST"]):
    print("new connection")
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
                state = game.state
                socketio.emit('update state', state, room=sid)
            else:
                print('login not successful')

@socketio.on('new url')
def handle_new_url()

@socketio.on('test')
def handle_test(msg, methods=["GET"]):
    print(msg)

@socketio.on('start trotting')
def start_trotting(ip, methods=["GET"]):
    for game in games:
        if game.ip == ip:
            game.state = "explore"
            print(f"The current state is {game.state}")

@socketio.on('stop trotting')
def stop_trotting(ip, methods=["GET"]):
    for game in games:
        if game.ip == ip:
            game.state = "idle"
            print(f"The current state is {game.state}")


if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True)