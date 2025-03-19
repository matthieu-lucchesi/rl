import pygame, pytmx, pyscroll
import pytmx.util_pygame

from src.map import MapManager
from src.entity import Entity, Player
from src.ath import Ath

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Survival AI - Shooter")

         #Add Sprites and Player
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self.all_sprites)

        
        self.map_manager = MapManager(self.screen, self.player)
        self.ath = Ath(self.player, )

    def handle_continuous_input(self):
        pressed = pygame.key.get_pressed()
        left_click, mouse_click, right_click = pygame.mouse.get_pressed()
        input = 0
        animation_on = self.player.attacking1 or ...
        if self.player.attacking1:
            return
        if pressed[pygame.K_z]:
            self.player.move_up()
            self.player.change_animation("up", action="Walk")
            input += 1
        if pressed[pygame.K_q]:
            self.player.move_left()
            self.player.change_animation("left", action="Walk")
            input += 1
        if pressed[pygame.K_s]:
            self.player.move_down()
            self.player.change_animation("down", action="Walk")
            input += 1
        if pressed[pygame.K_d]:
            self.player.move_right()
            self.player.change_animation("right", action="Walk")
            input += 1
        # if pressed[pygame.K_SPACE]:
        #     self.player.equipement["Helmet"] = 1 - self.player.equipement["Helmet"]
        #     input += 1
        if left_click:
            self.player.attack1()
        # if right_click:
        #     self.player.sword = not self.player.sword
        # if input == 0:
        #     self.player.change_animation(self.player.current_direction, action="Unarmed_Idle")

    def update(self):
        self.map_manager.update()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            # print(self.player.old_position, self.player.position)
            # self.player.save_position()
            self.handle_continuous_input()
            
            self.update()
            self.map_manager.draw()
            self.ath.render(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.equipement["Helmet"] = 1 - self.player.equipement["Helmet"]
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.player.sword = not self.player.sword
                    #     self.player.change_animation("left", action="Sword_Walk")
                    # if event.key == pygame.K_s:
                    #     self.player.move_down()
                    #     self.player.change_animation("down", action="Sword_Walk")
                    # if event.key == pygame.K_d:
                    #     self.player.move_right()
                    #     self.player.change_animation("right", action="Sword_Walk")

                        

            clock.tick(60)