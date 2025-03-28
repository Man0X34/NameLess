#-------------------------------------------------------------------------------
# Name:        main
# Purpose:     Charge la map, et l'affiche.
#
# Author:      Manoah
#
# Created:     28/03/2025
# Licence:     GPL v3+
#-------------------------------------------------------------------------------

import pygame
from pytmx import *

class MapLoader:
    def __init__(self, map_file="../data/asset/Map/map.tmx"):
        """Charge la carte TMX avec pytmx"""
        self.tmx_data = load_pygame(map_file)
        self.target_tile_size = 48  # Taille cible pour chaque tuile à l'écran
        self.collidable_tiles = []
        self.killable_tiles = []
        self.checkpoint_tiles = []
        self.map_width = self.tmx_data.width * self.target_tile_size
        self.map_height = self.tmx_data.height * self.target_tile_size

    def get_tile_gid(self, x, y):
        """Retourne le GID de la tuile à la position donnée"""
        if 0 <= x < self.tmx_data.width and 0 <= y < self.tmx_data.height:
            for layer in self.tmx_data:
                if isinstance(layer, TiledTileLayer):
                    gid = layer.data[y][x]
                    if gid:
                        return gid
        return 0

    def draw(self, target, collidable, killable, screen, camera_x=0, camera_y=0):
        """Dessine les tuiles à l'écran et gère les collisions."""
        layer = self.tmx_data.get_layer_by_name(target)
        
        if isinstance(layer, TiledTileLayer):
            for x, y, gid in layer.iter_data():
                if gid:  # Si la tuile existe (gid != 0)
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        # Position à l'écran (avec décalage caméra)
                        screen_x = x * self.target_tile_size - camera_x
                        screen_y = y * self.target_tile_size - camera_y
                        
                        if (-self.target_tile_size <= screen_x <= screen.get_width() and
                            -self.target_tile_size <= screen_y <= screen.get_height()):
                            
                            # Créer le rectangle par défaut
                            tile_rect = pygame.Rect(
                                x * self.target_tile_size,
                                y * self.target_tile_size,
                                self.target_tile_size,
                                self.target_tile_size
                            )

                            # Ajuster la hitbox en fonction du type de spike
                            if killable:
                                spike_divider = 2
                                if target == 'Top_spikes':
                                    tile_rect = pygame.Rect(
                                        x * self.target_tile_size,
                                        y * self.target_tile_size,
                                        self.target_tile_size,
                                        self.target_tile_size // spike_divider
                                    )
                                elif target == 'Bottom_spikes':
                                    tile_rect = pygame.Rect(
                                        x * self.target_tile_size,
                                        y * self.target_tile_size + (self.target_tile_size // spike_divider),
                                        self.target_tile_size,
                                        self.target_tile_size // spike_divider
                                    )
                                elif target == 'Left_spikes':
                                    tile_rect = pygame.Rect(
                                        x * self.target_tile_size,
                                        y * self.target_tile_size,
                                        self.target_tile_size // spike_divider,
                                        self.target_tile_size
                                    )
                                elif target == 'Right_spikes':
                                    tile_rect = pygame.Rect(
                                        x * self.target_tile_size + (self.target_tile_size // spike_divider),
                                        y * self.target_tile_size,
                                        self.target_tile_size // spike_divider,
                                        self.target_tile_size
                                    )
                                
                                self.killable_tiles.append((tile_rect, gid))
                            elif target == "Checkpoint":
                                self.checkpoint_tiles.append((tile_rect, gid))
                            elif collidable:
                                self.collidable_tiles.append((tile_rect, gid))

                            # Dessiner la tuile
                            scaled_tile = pygame.transform.scale(tile, (self.target_tile_size, self.target_tile_size))
                            screen.blit(scaled_tile, (screen_x, screen_y))
        
    def get_collidable_tiles(self):
        """Retourne la liste des tuples (rect, gid)"""
        return self.collidable_tiles

    def get_killable_tiles(self):
        """Retourne la liste des tuples (rect, gid)"""
        return self.killable_tiles
    
    def get_checkpoint_tiles(self):
        """Retourne la liste des tuples (rect, gid)"""
        return self.checkpoint_tiles
    
    def debug(self, screen, camera_x=0, camera_y=0):
        """DEBUG: Afficher les rectangles de collision avec décalage caméra"""
        collidable_tiles = self.get_collidable_tiles()
        killable_tiles = self.get_killable_tiles()
        for tile,gid in collidable_tiles:
            debug_rect = pygame.Rect(
                tile.x - camera_x,
                tile.y - camera_y,
                tile.width,
                tile.height
            )
            pygame.draw.rect(screen, (0, 0, 255), debug_rect, 2)
        for tile,gid in killable_tiles:
            debug_rect = pygame.Rect(
                tile.x - camera_x,
                tile.y - camera_y,
                tile.width,
                tile.height
            )
            pygame.draw.rect(screen, (0, 0, 255), debug_rect, 2)
            
    def get_player_start_position(self):
        """Retourne la position de départ du joueur depuis le calque Player"""
        player_layer = self.tmx_data.get_layer_by_name('Start')
        
        if isinstance(player_layer, TiledTileLayer):
            # Parcourir le calque pour trouver le premier tile non vide (gid != 0)
            for y in range(player_layer.height):
                for x in range(player_layer.width):
                    gid = player_layer.data[y][x]
                    if gid != 0:  # Si on trouve une tuile
                        # Convertir les coordonnées de tuile en pixels
                        pixel_x = x * self.target_tile_size
                        pixel_y = y * self.target_tile_size
                        return pixel_x, pixel_y
        # Position par défaut si rien n'est trouvé
        return 100, 100
