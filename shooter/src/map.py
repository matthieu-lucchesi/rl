from dataclasses import dataclass  # Class without any methods

import pygame, pytmx, pyscroll


@dataclass
class Portal:
    from_world: str
    from_point: str
    dest_world: str
    dest_point: str


@dataclass  
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]

class MapManager:
    def __init__(self, screen, player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "world"

        self.register_map("world", portals=[
            Portal(from_world="world", from_point="enter_house1", dest_world="house1", dest_point="enter_house1_spawn"),
            Portal(from_world="world", from_point="enter_house2", dest_world="house2", dest_point="enter_house2_spawn"),
            Portal(from_world="world", from_point="enter_dungeon1", dest_world="dungeon1", dest_point="enter_dungeon1_spawn"),
            Portal(from_world="world", from_point="enter_fight_world", dest_world="fight_world", dest_point="enter_fight_world_spawn"),
        ])
        self.register_map("house1", portals=[
            Portal(from_world="house1", from_point="exit_house1", dest_world="world", dest_point="exit_house1_spawn")
        ])
        self.register_map("house2", portals=[
            Portal(from_world="house2", from_point="exit_house2", dest_world="world", dest_point="exit_house2_spawn")
        ])
        self.register_map("dungeon1", portals=[
            Portal(from_world="dungeon1", from_point="exit_dungeon1", dest_world="world", dest_point="exit_dungeon1_spawn")
        ])
        self.register_map("fight_world", portals=[
            Portal(from_world="fight_world", from_point="exit_fight_world", dest_world="world", dest_point="exit_fight_world_spawn")
        ])
        
        self.teleport_player("player")
    
    def check_collisions(self):
        #Portals
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.from_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.dest_world
                    self.teleport_player(copy_portal.dest_point)

        #Collisions
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()
    
    
    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x - self.player.rect.width // 2
        self.player.position[1] = point.y - self.player.rect.height // 2
        self.player.save_position()


    def register_map(self, name, portals=[]):
        #Load map
        tmx_data = pytmx.util_pygame.load_pygame(f"shooter/assets/maps/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layers = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layers.zoom = 2

        #Collision list
        walls = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        #Draw layers group
        layer_index = -1
        for layer in list(tmx_data.layers):
            if layer.name == "above_player":
                break 
            layer_index +=1
        group = pyscroll.PyscrollGroup(map_layer=map_layers, default_layer=layer_index)  # TODO This is not working, always first taken for PyscrollGroup
        group.add(self.player)
        group.add(self.player.all_sprites)
        
        # Create map
        self.maps[name] = Map(name, walls, group, tmx_data, portals)

    def get_map(self): return self.maps[self.current_map]
    def get_group(self): return self.get_map().group
    def get_walls(self): return self.get_map().walls
    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)


    def update(self):
        self.get_group().update()
        self.check_collisions()
