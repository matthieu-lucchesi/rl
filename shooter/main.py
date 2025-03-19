import pygame

from src.game import Game

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()

    


# TODO imporve :
# - be able to equip or unequip items ... (make them more smooth)
# - ATH for player (HP, mana, XP, defense, spd) (need imprevements ...)
# - attack with sword (need to add with equipement)
# - moove ennemies ()


# DONE:
# - spawn ennemies

# TODO :
# - attack ennemies
# - take damage