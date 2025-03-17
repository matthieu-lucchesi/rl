import os
import time
import pygame

from src.animation import AnimatedSprite

class Entity(AnimatedSprite):
    def __init__(self, name, x, y, hpmax=100, armor=10, speed=10, manamax=10, attack=86):
        super().__init__(name)
        self.equipement = {}
        self.stats = {
        "hpmax" : hpmax,
        "armor" : armor,
        "speed" : speed,
        "manamax" : manamax,
        "attack" : attack,
        "hp" : hpmax,
        "mana" : manamax,
        }

        self.change_animation("down")
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width // 4, self.rect.height // 5)
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
        self.feet.center = self.rect.center 
        self.feet.y += self.rect.height // 8


class Player(Entity):
    def __init__(self, all_sprites):
        super().__init__("player/", 0, 0)
        self.all_sprites = all_sprites
        self.equipement = {
            "Helmet" : 0,
            # "Boots" : 0,
            # "Chest": 0,
        }
        self.equipement_images = {
            "down": {}, 
            "left": {},
            "right": {},
            "up": {},
        }
        self.current_action = "Unarmed_Idle"
        self.attacking1 = False
        self.attack_timer = 0  # Timer to control attack animation speed

        self.get_equipement_paths()
        for equipement in self.equipement_action_dict.keys():
            for action, path in self.equipement_action_dict[equipement].items():
                for direction in self.equipement_images.keys():
                    if action not in self.equipement_images[direction].keys():
                        self.equipement_images[direction][action] = {}
                self.get_equipements(action, equipement, path, size=[64,64])
        
        # Create Sprites
        self.equipement_group = pygame.sprite.Group()  
        self.equipement_sprites = {}  

        for equipement in self.equipement.keys():
            images = {direction: {action: frames.get(equipement, [])  # ✅ Utiliser `.get()` pour éviter KeyError
                    for action, frames in self.equipement_images[direction].items()}
                    for direction in self.equipement_images}

            sprite = EquipmentSprite(self, equipement, images)
            self.equipement_sprites[equipement] = sprite
            self.all_sprites.add(sprite)  


    def get_equipement_paths(self):
        """store in self.equipement_action_dict[equipement][action] paths"""
        self.equipement_action_dict = {}
        for equipement in os.listdir("shooter/assets/player/equipement/"):
            equipement_path = "shooter/assets/player/equipement/" + equipement
            self.equipement_action_dict[equipement] = {}
            for file_path in os.listdir(equipement_path):
                if f"_{equipement}" not in file_path:
                    continue  # skip if file
                action = file_path.split(f"_{equipement}")[0]
                self.equipement_action_dict[equipement][action] = equipement_path + '/' + file_path
                # for direction in self.equipement.keys():
                #     self.equipement[direction][action][equipement] = equipement_path

    def get_equipements(self, action, equipement, path, size=[64,64]):
        """store in self.equipements[direction][action]["equipement"] frames from path"""
        def get_image(sprite_sheet, x, y, size):
            image = pygame.Surface(size)
            image.blit(sprite_sheet, (0, 0), (x, y, size[0], size[1])) 
            image.set_colorkey((0, 0, 0))
  
            return image
        sprite_sheet = pygame.image.load(path)
        directions = ["down", "left", "right", "up"]
        sheet_size = sprite_sheet.get_size()
        for y in range(0, sheet_size[1], size[1]):
            images = [] 
            for x in range(0, sheet_size[0], size[0]):
                image = get_image(sprite_sheet, x, y, size)
                images.append(image)
            self.equipement_images[directions[y // size[1]]][action][equipement] = images
    
    def attack1(self):
        if self.attacking1:
            return  # Break if already attacking
        self.attacking1 = True
        self.current_action = "Sword_Walk_Attack"
        self.animation_index = 0
        self.attack_timer = time.time()  # Start attack timer

        for equipement, sprite in self.equipement_sprites.items():
            if self.equipement[equipement]:  # If the equipment is active
                sprite.update()  # Force update equipment sprite

    def update_equipement(self):
        """Active ou désactive les équipements en fonction de leur état."""
        for equipement, equipped in self.equipement.items():
            sprite = self.equipement_sprites[equipement]
            sprite.visible = equipped
            sprite.update()

    def update(self):
        """Met à jour le joueur et ses équipements."""
        super().update()
        self.update_equipement()
        print(self.attacking1, self.animation_index)
        if self.attacking1:
            if time.time() - self.attack_timer > 0.05:  # Change de frame toutes les 0.1s
                self.attack_timer = time.time()  # Réinitialise le timer
                self.animation_index += 1

                # Vérifie si l'animation est terminée
                if self.animation_index >= len(self.images[self.current_direction][self.current_action]):
                    self.attacking1 = False  # Fin de l'attaque
                    self.current_action = "Unarmed_Walk"
                    self.animation_index = 0  # Remet à la première frame
                else:
                    # Met à jour l'image du joueur
                    self.image = self.images[self.current_direction][self.current_action][self.animation_index]
                    self.image.set_colorkey([0, 0, 0])

                    # Met à jour l'équipement
                    for equipement, sprite in self.equipement_sprites.items():
                        if self.equipement[equipement]:  
                            sprite.image = sprite.images[self.current_direction][self.current_action][self.animation_index]


class EquipmentSprite(pygame.sprite.Sprite):
    def __init__(self, player, equipement_name, images):
        super().__init__()
        self.player = player  # Le joueur auquel l'équipement est attaché
        self.equipement_name = equipement_name  
        self.images = images  # Dictionnaire des frames d'animation
        self.image = self.images[self.player.current_direction][self.player.current_action][0] 
        self.rect = self.image.get_rect()
        self.feet = player.feet
        self.visible = False  # Equipement not visible if unequipped

    def update(self):
        if not self.visible:
            self.image = pygame.Surface((0, 0)) # Rendre invisible
            return
        
        direction = self.player.current_direction  
        action = self.player.current_action  
        
        if direction in self.images and action in self.images[direction]:  
            frames = self.images[direction][action]  
            if frames and len(frames) > self.player.animation_index:  
                self.image = frames[self.player.animation_index]
        self.rect.topleft = self.player.rect.topleft




class Ennemy(Entity, ):
    def __init__(self, name,):
        super().__init__(name, 0, 0)
    
