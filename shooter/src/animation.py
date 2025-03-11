import pygame

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f"shooter/assets/player/{name}.png")
        self.animation_index = 0
        self.speed = 3
        self.clock = 0
        self.images={
            "down": self.get_images(0),  # Only y is needed
            "left": self.get_images(32),
            "right": self.get_images(64),
            "up": self.get_images(96),
        }
    
    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))   
        return image
    
    def get_images(self, y):
        images = []
        for i in range(3):
            x = i * 32
            image = self.get_image(x, y)
            images.append(image)
        return images
    
    def change_animation(self, name):
        print(self.animation_index)
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey([0, 0, 0])
        self.clock += self.speed * 15
        if self.clock % 100 == 0:
            self.animation_index = (self.animation_index + 1) % len(self.images[name])