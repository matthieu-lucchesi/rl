import pygame

class Ath():
    def __init__(self, player):
        self.player = player
        self.box = pygame.image.load("shooter/assets/dialogs/ath.png").convert_alpha()
        self.update_hp_bar()
        self.update_mana_bar()
        self.update_stats()
        

    def render(self, screen):
        self.box_scaled = pygame.transform.scale(self.box, (self.box.get_width() * 2, self.box.get_height() * 2))
        screen_width, screen_height = screen.get_size() 
        box_width, box_height = self.box_scaled.get_size() 

        x = (screen_width - box_width) // 2  
        y = screen_height - box_height  

        screen.blit(self.box_scaled, (x, y))


    def update_hp_bar(self):
        self.hpmax_bar = pygame.draw.rect(self.box, (255, 0, 0,255), (80, 28, 113,4))
        width = int((self.player.stats["hp"] / self.player.stats["hpmax"]) * self.hpmax_bar.width) - 50
        self.hb_bar = pygame.draw.rect(self.box, (0, 255, 0,255), (80, 28, width,4))

    def update_mana_bar(self):
        self.manamax_bar = pygame.draw.rect(self.box, (255, 0, 0,255), (80, 35, 113, 4))
        width = int((self.player.stats["mana"] / self.player.stats["manamax"]) * self.manamax_bar.width) - 2
        self.mana_bar = pygame.draw.rect(self.box, (0, 0, 255,255), (80, 35, width, 4))
    
    def update_stats(self):
        self.font = pygame.font.Font(None, 10)  
        color = (67, 56, 37)
        attack_text = self.font.render(str(self.player.stats["attack"]), True, color)
        armor_text = self.font.render(str(self.player.stats["armor"]), True, color)
        speed_text = self.font.render(str(self.player.stats["speed"]), True, color)
        self.box.blit(attack_text, (16, 9))
        self.box.blit(armor_text, (35, 9))
        self.box.blit(speed_text, (35, 24))