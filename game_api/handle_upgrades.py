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