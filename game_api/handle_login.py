import player
from cryptography.fernet import Fernet

############################################################################
### Library for processing a user's login attempt and instantiating them ###
############################################################################

# General handler for taking and processing login attempts
# This entire library will likely change a lot when the front end attaches
# Upon sucessful login, set game.state to "explore"
def handle_login(self):
    # if self.state == "initialize":
    #     login_info = get_login_info()
    #     is_valid = validate_login_info(login_info)
    #     if is_valid:
    #         user = fetch_user_info(self.players, login_info[0])
    #         self.player = generate_player(user)
    #         self.instantiate_party()
    #         self.state = "explore"

    if self.state == "initialize":
        password = fetch_user_info(self.players, self.username)
        if password:
            valid = compare_passwords(self.password, self.secret_key, password)
            # password = encrypt_password(self.password, self.secret_key)
            if valid:
                print("Passwords match")
                self.state = "idle"
            elif not valid:
                print("Password does not match")
        else:
            print("Username not found")


def encrypt_password(password, key):
    encrypted_pw = encrypt_message(password, key)
    return encrypted_pw

def encrypt_message(message, key):
    """
    Encrypts a message
    """
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message

def fetch_user_info(players, username):
    user = players.find({"username": username})
    for doc in user:
        if doc["username"] == username:
            password = doc["password"]
            return password

def compare_passwords(password, key, encrypted_password):
    b_string = bytes(password, encoding=("UTF-8"))
    decrypted_password = decrypt_message(encrypted_password, key)
    print(decrypted_password)
    print(b_string)
    if decrypted_password == b_string:
        return True
    else:
        return False

def decrypt_message(encrypted_message, key):
    """
    Decrypts an encrypted message
    """
    f = Fernet(key)
    b_string = bytes(encrypted_message, encoding='UTF-8')
    decrypted_message = f.decrypt(b_string)
    return decrypted_message

# With the info taken from the database, generate a player instance
def generate_player(user):
    new_user = player.Player()
    for doc in user:
        new_user.username = doc["username"]
        new_user.collection = doc["collection"]
    return new_user