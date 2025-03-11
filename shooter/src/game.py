import pygame, pytmx, pyscroll
import pytmx.util_pygame

from src.map import MapManager
from src.entity import Entity, Player


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Survival AI - Shooter")

         #Add player
        self.player = Player() #player_position.x, player_position.y)
        self.map_manager = MapManager(self.screen, self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_z]:
            self.player.move_up()
            self.player.change_animation("up")
        if pressed[pygame.K_q]:
            self.player.move_left()
            self.player.change_animation("left")
        if pressed[pygame.K_s]:
            self.player.move_down()
            self.player.change_animation("down")
        if pressed[pygame.K_d]:
            self.player.move_right()
            self.player.change_animation("right")


    def update(self):
        self.map_manager.update()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.player.save_position()
            self.handle_input()
            
            self.update()
            self.map_manager.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)