from flask import Flask, request, json, Response, render_template
from flask_cors import CORS


from game import Game

game = Game()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'

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

@app.route('/send')
def send_py_data():
    return json.dumps("String")

if __name__ == "__main__":
    app.run(port=5000, debug=True)