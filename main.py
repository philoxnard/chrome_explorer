import game

if __name__ == "__main__":

    game = game.Game()

    while True:
        if game.state == "initialize":
            game.handle_login()
        if game.state == "explore":
            # This is for testing purposes only, gonna have to find a way
            # To only run new_url_handler when a new url appears
            game.player.url = input("type a new url ")
            game.new_url_handler()
        if game.state == "initialize_encounter":
            game.initialize_encounter()
        if game.state == "encounter":
            game.combat()
            # Server will run calcs to determine whose turn it is - add up speed from each mon until someone hits 100
            # If enemy's turn, server will pick an attack and execute
            # If player's turn, server will tell browser what options player has
            # Server will take input and decide what to do based on it
                # If run, server will give browser an end-the-fight message and set game.state to "explore"
                # If swap, server will give browser a menu of who to swap to based on user collection
                # If attack, server will take the attack and run calcs to assign damage/status effects
            # If player mon dies, force swap or run
            # If enemy mon dies, set game.state to "encounter_cleanup"
        if game.state == "encounter_cleanup":
            # Server will calculate experience gain for the active mon
            # Server will add enemy mon to user's collection
            # Server will set game.state to "explore"
            pass

# This is just the base framework for the game.
# This file will not actually be used in the actual release version of the game
# This file is only meant for planning purposes, and potentially for play testing
# here in the Python terminal before the actual front-end is set up or connected
# As it gets developed, new features will be added such as:
    # Buttons in browser to naviage through a user's party and a user's collection
    # Option for players to battle each other
    # Some kind of general story, or at least a kind of gym battle system

