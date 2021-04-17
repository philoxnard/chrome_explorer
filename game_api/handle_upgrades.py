from upgrades import get_upgrade_effects
from game_api.experience import store_phox_in_db

########################################################################
### Library for handling a click on an upgrade in the view Phox menu ###
########################################################################

# General handler for when an upgrade is clicked.
# Already been verified that the phox exists and is in the user's party
def select_upgrade(self, phox, row, option):
    if len(phox.upgrade_indexes) == int(row):
        if int(row) <= (phox.level - 1):
            phox.upgrade_indexes.append(option)
            upgrade_string = phox.upgrade_tree[row][option].name
            get_upgrade_effects(upgrade_string, phox, self.upgrades)
            store_phox_in_db(phox, self.player, self.players)
            return True

    # Check to see how long phox.upgrade_indexes is
    # Check to see what level the phox is
    # if row > (phox.level-1):
        # do nothing
    # if row = len(phox.upgrade_index)
        # do something
        # bc len(phox.upgrade_index) will be 0 after resetting, so you start at row 0
        # then as you get each upgrade, the length will go up by one, allowing you to 
        # get the next one
        # phox.upgrade_index.append(option)
        # THEN:
            # Get the string of the new upgrade
                # should be phox.upgrade_tree[row][option].name
                # get_upgrade_effects(upgrade_string, phox, upgradeDB)
            # Store new phox in database
            # send message back to the client to 'activate' that upgrade
                # have this return True if the upgrade actually gets activated
                # server will have something like:
                # If True:
                    # socketio.emit('activate upgrade', row, option, sid)
                    # ACTUALLY, can probably just redraw the upgrade tree
                    # with an existing function, and it'll see that the upgrade
                    # has been activated and will ddraw it accordingly