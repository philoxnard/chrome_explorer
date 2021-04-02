from flask import Flask, request, json, Response, render_template, session
from flask_cors import CORS


from game import Game

game = Game()

app = Flask(__name__)
CORS(app)
app.secret_key = 'vnkdjnfjknfl1232#'

@app.route('/login', methods=["GET", "POST"])
def handle_login():
    if game.state == "initialize":
        if request.method == "POST":
            game.username = request.form["username"]
            game.password = request.form["password"]
            game.handle_login()
            if game.state == "idle":
                print('state is idle')
                return "success", 200
            else:
                return "fail", 200
    
    if game.state == "idle":
        return "success", 200

@app.route('/check_state', methods=["GET"])
def handle_state_check():
    print(f"The current state is {game.state}")
    return game.state, 200

@app.route('/start_trotting', methods=["GET"])
def start_trotting():
    game.state = "explore"
    print(f"The current state is {game.state}")
    return 'success', 200

@app.route('/send')
def send_py_data():
    return json.dumps("String")

if __name__ == "__main__":
    app.run(port=5000, debug=True)