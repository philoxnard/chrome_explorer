import player

############################################################################
### Library for processing a user's login attempt and instantiating them ###
############################################################################

# General handler for taking and processing login attempts
# This entire library will likely change a lot when the front end attaches
def handle_login(self):
    login_info = get_login_info()
    is_valid = validate_login_info(login_info)
    if is_valid:
        user = fetch_user_info(self.players, login_info[0])
        player = generate_player(user)
        return player

# This will change when the front end is attached
def get_login_info():
    username = input("Whats your username? ")
    password = input("Whats your password? ")
    login_info = [username, password]
    return login_info

# This will change when I know how to validate logins in Python
def validate_login_info(login_info):
    return True

# After the login attempt is successful, take the username and find the appropraite player info
def fetch_user_info(players, username):
    user = players.find({"username": username})
    return user

# With the info taken from the database, generate a player instance
def generate_player(user):
    new_user = player.Player()
    for doc in user:
        new_user.username = doc["username"]
        new_user.collection = doc["collection"]
        new_user.party = doc["party"]
    return new_user