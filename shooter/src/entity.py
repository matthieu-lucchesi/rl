import pygame

from src.animation import AnimatedSprite

class Entity(AnimatedSprite):
    def __init__(self, name, x, y):
        super().__init__(name)
        
        self.change_animation("down")
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width // 2, self.rect.height // 3)
        self.old_position = self.position.copy()

    
    
    def save_position(self): self.old_position = self.position.copy()

    

    def move_up(self): self.position[1] -= self.speed
    def move_left(self): self.position[0] -= self.speed
    def move_down(self): self.position[1] += self.speed
    def move_right(self): self.position[0] += self.speed


    def move_back(self):
        """Cancel move."""
        self.position = self.old_position
        self.update()

    def update(self):  # Called by group.update()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


class Player(Entity):
    def __init__(self):
        super().__init__("Player", 0, 0)

class NPC(Entity, ):
    def __init__(self, name,):
        super().__init__(name, 0, 0)
