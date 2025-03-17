# Project Notes

## Classes

### **Game**
* Attributes:
    - **screen** : *Main object to display*
    - **all_sprites** : *pygame.sprite.Group object containing all dynamic objects*
    - **player** : *Main character of the game. From class Player*
    - **map_manager** : *Handle the environment where the player is. From class MapManager*

* Methods:
    - **handle_input**() : *Loop over pressed keys and make something depending on which key is pressed*
    - **update**() : *Update the game, mainly calling map_manager.update()*
    - **run**() : *Application loop, handle fps and calling game functions in the right order*


### **MapManager**
* Dataclasses :
    - **Portal**(from_world: str, from_point: str, dest_world: str, dest_point: str) : *Attributes for portal dataclass used in MapManager to handle portals between points (used when changing world)*

    - **Map**(name: str, walls: list[pygame.Rect], group: pyscroll.PyscrollGroup, tmx_data: pytmx.TiledMap, portals: list[Portal]) : *Attributes for Map dataclass used in MapManager to store all maps in the game (houses, dungeons, etc...)*

* Attributes:
    - **maps**
    - **screen** 
    - **player**
    - **current_map** 

* Methods :
    - **check_collisions**():
    - **teleport_player**(name): *Name is the point where to teleport the player*
    - **register_map**(name, portals=[]): *Store a map with a name and portals*
    - **get_map**(): 
    - **get_group**(): 
    - **get_walls**(): 
    - **get_object**(name): 
    - **draw**():
    - **update**():




### Game
* attributes:
    - **screen** : **
    - **all_sprites** : **
    - **player** : **
    - **map_manager** : **

* Methods:
    - **handle_input**() : **
    - **update**() : **
    - **run**() : **






# Pygame Cheat Sheet

## 1. Initialisation de Pygame
```python
import pygame
pygame.init()
```

## 2. Création d'une Fenêtre
```python
screen = pygame.display.set_mode((800, 600))  # Taille de la fenêtre
pygame.display.set_caption("Mon Jeu Pygame")  # Titre de la fenêtre
```

## 3. Utilisation des Rect
### Qu'est-ce qu'un Rect ?
Un `Rect` est une structure rectangulaire qui facilite la gestion des positions, collisions et transformations.
```python
player_rect = pygame.Rect(100, 100, 50, 50)  # (x, y, largeur, hauteur)
```
### Avantages de `Rect` :
- Gestion simplifiée des collisions (`colliderect`, `collidepoint`)
- Manipulation facile (`move`, `inflate`, `clamp`)

### Fonctions utiles
```python
player_rect.move_ip(5, 0)   # Déplacer à droite de 5 pixels
player_rect.inflate_ip(10, 10)  # Augmenter la taille
```

## 4. Gérer les Mouvements
```python
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:
    player_rect.x -= 5
if keys[pygame.K_RIGHT]:
    player_rect.x += 5
if keys[pygame.K_UP]:
    player_rect.y -= 5
if keys[pygame.K_DOWN]:
    player_rect.y += 5
```

## 5. Affichage avec `blit()` et `draw()`
```python
# Charger une image
player_img = pygame.image.load("player.png")
screen.blit(player_img, player_rect)

# Dessiner un rectangle
pygame.draw.rect(screen, (255, 0, 0), player_rect)
```

## 6. Rafraîchir l'écran avec `flip()` et `update()`
```python
pygame.display.flip()  # Rafraîchir toute la fenêtre
# OU
pygame.display.update()  # Peut mettre à jour une partie de l'écran
```

## 7. Boucle de Jeu
```python
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))  # Effacer l'écran
    screen.blit(player_img, player_rect)  # Dessiner le joueur
    pygame.display.flip()  # Rafraîchir l'affichage

pygame.quit()
```

## 8. Gérer les Collisions
```python
if player_rect.colliderect(obstacle_rect):
    print("Collision!")
```

## 9. Ajouter un Timer (FPS)
```python
clock = pygame.time.Clock()
while running:
    clock.tick(60)  # Limite à 60 FPS
```

## 10. Jouer un Son
```python
pygame.mixer.init()
sound = pygame.mixer.Sound("sound.wav")
sound.play()
```

