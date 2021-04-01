import game

if __name__ == "__main__":

    game = game.Game()

    while True:
        if game.state == "initialize":
            game.terminal_test_login()
        if game.state == "explore":
            # This is for testing purposes only, gonna have to find a way
            # To only run new_url_handler when a new url appears
            game.player.url = input("type a new url ")
            game.new_url_handler()
        if game.state == "initialize encounter":
            game.initialize_encounter()
        if game.state == "encounter":
            game.combat()
        if game.state == "encounter cleanup":
            game.encounter_cleanup()

# This is just the base framework for the game.
# This file will not actually be used in the actual release version of the game
# This file is only meant for planning purposes, and potentially for play testing
# here in the Python terminal before the actual front-end is set up or connected
# As it gets developed, new features will be added such as:
    # Buttons in browser to naviage through a user's party and a user's collection
    # Option for players to battle each other
    # Some kind of general story, or at least a kind of gym battle system

