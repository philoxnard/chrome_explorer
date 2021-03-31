from flask import Flask, render_template, jsonify, request, make_response
from flask_cors import CORS


from game import Game

game = Game()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'

@app.route('/login', methods=["GET", "POST"])
def handle_login():
    if request.method == "POST":
        username = request.form["username"]
        print(username)
        return 'Success', 200

@app.route('/test', methods=["POST"])
def test_func():
    data = request.form["data"]
    print(f"Does this work? {data}")
    return 'Success', 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)