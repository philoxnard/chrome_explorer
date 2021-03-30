

###########################################################
### Library for handling visits to the Phoxtrot website ###
###########################################################


def handle_phoxtrot_site(self):
    self.player.shutdown = False
    for phox in self.player.party:
        phox.disconnected = False
        phox.stats["health"] = phox.max_health
        phox.status = None
    print('healing your phoxes')