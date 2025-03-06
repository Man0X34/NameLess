import pygame
from pytmx import *

class MapLoader:
    def __init__(self, map_file="map.tmx"):
        """Charge la carte TMX avec pytmx"""
        self.tmx_data = load_pygame(map_file)
        self.target_tile_size = 48  # Taille cible pour chaque tuile à l'écran
        self.collidable_tiles = []

        self.map_width = self.tmx_data.width * self.target_tile_size
        self.map_height = self.tmx_data.height * self.target_tile_size

    def is_tile_at(self, x, y):
        """Vérifie si une tuile existe à la position donnée"""
        if 0 <= x < self.tmx_data.width and 0 <= y < self.tmx_data.height:
            for layer in self.tmx_data.visible_layers:
                if isinstance(layer, TiledTileLayer):
                    if layer.data[y][x]:
                        return True
        return False

    def draw(self, screen, camera_x=0, camera_y=0):
        """Dessine la carte à l'écran avec un décalage"""
        self.collidable_tiles.clear()
        screen_width, screen_height = screen.get_size()
        
        # Calculer les tuiles visibles uniquement
        start_x = max(0, camera_x // self.target_tile_size)
        end_x = min(self.tmx_data.width, (camera_x + screen_width) // self.target_tile_size + 1)
        start_y = max(0, camera_y // self.target_tile_size)
        end_y = min(self.tmx_data.height, (camera_y + screen_height) // self.target_tile_size + 1)

        adjustment = 8  # Nombre de pixels à retirer sur les bords exposés
        radius = 12    # Rayon pour les coins arrondis

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, TiledTileLayer):
                for x in range(int(start_x), int(end_x)):
                    for y in range(int(start_y), int(end_y)):
                        gid = layer.data[y][x]
                        if gid:
                            tile = self.tmx_data.get_tile_image_by_gid(gid)
                            if tile:
                                # Position à l'écran avec décalage caméra
                                screen_x = x * self.target_tile_size - camera_x
                                screen_y = y * self.target_tile_size - camera_y

                                # Ajuster le rect en fonction des tuiles adjacentes
                                rect_x = x * self.target_tile_size
                                rect_y = y * self.target_tile_size
                                rect_width = self.target_tile_size
                                rect_height = self.target_tile_size

                                # Créer un Rect pour la collision
                                tile_rect = pygame.Rect(
                                    rect_x,
                                    rect_y,
                                    rect_width,
                                    rect_height
                                )
                                self.collidable_tiles.append(tile_rect)
                                
                                # Dessiner la tuile
                                scaled_tile = pygame.transform.scale(tile, (self.target_tile_size, self.target_tile_size))
                                screen.blit(scaled_tile, (screen_x, screen_y))
                                
                                # DEBUG: Dessiner le rect de collision avec coins arrondis
                                debug_rect = pygame.Rect(
                                    tile_rect.x - camera_x,
                                    tile_rect.y - camera_y,
                                    tile_rect.width,
                                    tile_rect.height
                                )

                                # Dessiner le rectangle principal
                                pygame.draw.rect(screen, (0, 0, 255), debug_rect, 1)

    
    def get_collidable_tiles(self):
        return self.collidable_tiles
                        
    


