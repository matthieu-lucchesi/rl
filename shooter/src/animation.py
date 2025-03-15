import pygame.locals
import pygame, pytmx, os
import pytmx.util_pygame

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        # self.sprite_sheet = pygame.image.load(f"shooter/assets/player/{name}.png")
        self.get_sprite_sheet(f"shooter/assets/{name}")

        # self.sprite_sheet_size = [32, 32]
        self.animation_index = 0
        self.speed = 3
        self.clock = 0
        self.images = {
            "down": {}, 
            "left": {},
            "right": {},
            "up": {},
        }
        self.current_direction = "down"

        for key, path in self.dict_action_path.items():
            self.get_images(key, path, [64, 64])

    def get_sprite_sheet(self, dir):
        """Retuns dict["action": path_to_action_full.png, ...]"""
        dir += "base/"
        self.dict_action_path = {}
        for path in os.listdir(dir):
            fpath = dir + path
            if os.path.isfile(fpath) and "_full" in path:
                self.dict_action_path[path.split("_full")[0]] = fpath

    
    def get_images(self, key, path, size=[64,64]):
        """store in self.images["direction][action] frames from path"""
        def get_image(sprite_sheet, x, y, size):
            image = pygame.Surface(size)
            image.blit(sprite_sheet, (0, 0), (x, y, size[0], size[1]))   
            return image
        sprite_sheet = pygame.image.load(path)
        directions = ["down", "left", "right", "up"]
        sheet_size = sprite_sheet.get_size()
        for y in range(0, sheet_size[1], size[1]):
            images = [] 
            for x in range(0, sheet_size[0], size[0]):
                image = get_image(sprite_sheet, x, y, size)
                images.append(image)
            self.images[directions[y // size[1]]][key] = images

    def change_animation(self, direction, action="Unarmed_Walk"):
        self.image = self.images[direction][action][self.animation_index]
        self.image.set_colorkey([0, 0, 0])
        self.current_direction = direction
        self.clock += self.speed * 15
        if self.clock % 100 == 0:
            self.animation_index = (self.animation_index + 1) % len(self.images[direction][action])
            


