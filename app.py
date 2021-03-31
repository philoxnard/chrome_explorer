from flask import Flask, render_template, jsonify

from game import Game
game = Game()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'

@app.route('/')
def sessions():
    text = game.regions
    x = text.find({"region": "streaming"})
    for doc in x:
        return doc["domains"][0]

if __name__ == "__main__":
    app.run(debug=True)