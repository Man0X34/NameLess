import pygame
from pytmx import *

class MapLoader:
    def __init__(self, map_file="map.tmx"):
        """Charge la carte TMX avec pytmx"""
        self.tmx_data = load_pygame(map_file)
        self.target_tile_size = 48  # Taille cible pour chaque tuile à l'écran
        self.collidable_tiles = []

    def draw(self, screen, offset_x=0, offset_y=0):
        """Dessine la carte à l'écran avec un décalage"""
        screen_width, screen_height = screen.get_size()
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        # Redimensionner la tuile
                        screen_x = x * self.target_tile_size + offset_x
                        screen_y = y * self.target_tile_size + offset_y
                        # Créer un Rect pour la tuile
                        tile_rect = pygame.Rect(screen_x, screen_y, self.target_tile_size, self.target_tile_size)
                        self.collidable_tiles.append(tile_rect)
                        if 0 <= screen_x < screen_width and 0 <= screen_y < screen_height:
                            
                            # Redimensionner et dessiner la tuile
                            scaled_tile = pygame.transform.scale(tile, (self.target_tile_size, self.target_tile_size))
                            screen.blit(scaled_tile, (screen_x, screen_y))
    
    
    def get_collidable_tiles(self):
        return self.collidable_tiles
