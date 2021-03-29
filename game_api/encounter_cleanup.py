


def encounter_cleanup(self):
    print('encounter is over')
    for phox in self.player.party:
        phox.can_act = False
        phox.is_attacking = False
        phox.RAM = phox.max_RAM
    print("Returning to explore state")
    self.state = "explore"