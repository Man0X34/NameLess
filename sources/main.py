#Projet : NameLess
#Auteurs : Manoah Avril, Link Bernard, Noa Paté

import pygame
from player import *
from menu import *
from map_loader import *
import os

# Force le fichier à s'ouvrir dans son dossier (car sinon il s'ouvre n'importe où et ne trouve pas les fichiers)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
debug_mode = False
sound = True

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.is_fullscreen = True # Commencer avec les bordures
        self.window_size = (1300, 900)  # Taille en mode fenêtré normal
        self.map_loader = MapLoader()
        
        # Obtenir et stocker la position de départ du joueur
        self.spawn = self.map_loader.get_player_start_position()
        self.player = Player(self.spawn[0], self.spawn[1])
        
        # Liste des plateformes (sols)
        self.collidable_tiles = self.map_loader.get_collidable_tiles()
        self.killable_tiles = self.map_loader.get_killable_tiles()
        
        self.camera_x = 0
        self.camera_y = 0
        if sound:
            # Initialiser et jouer la musique
            pygame.mixer.init()
            pygame.mixer.music.load("../data/asset/audio/Forest-Under-The-Great-Tree-_Extended.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

    def toggle_window_mode(self):
        if self.is_fullscreen:
            # Mode FULLSCREEN
            self.screen = pygame.display.set_mode(
                (0, 0),
                pygame.FULLSCREEN
            )
        else:
            # Mode fenetré
            self.screen = pygame.display.set_mode(self.window_size)
        self.is_fullscreen = not self.is_fullscreen

    def handling_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:  # F11 pour basculer
                    self.toggle_window_mode()
                elif event.key == pygame.K_ESCAPE:  # Échap pour quitter
                    self.running = False

    def update_camera(self):
        # Obtenir les dimensions de l'écran
        screen_width, screen_height = self.screen.get_size()
        
        # Centrer la caméra sur le joueur
        target_x = self.player.rect.centerx - screen_width // 2
        target_y = self.player.rect.centery - screen_height // 2
        
        # Limites de la carte
        max_camera_x = self.map_loader.map_width - screen_width
        max_camera_y = 20*48
        
        # Appliquer les limites
        self.camera_x = max(0, min(target_x, max_camera_x))
        self.camera_y = max(0, min(target_y, max_camera_y))

    def update(self):
        dt = self.clock.get_time() / 1000.0  # Obtenir le temps écoulé en secondes
        self.player.move(self.collidable_tiles, dt)
        self.player.update(self.collidable_tiles, self.killable_tiles, self.map_loader.get_checkpoint_tiles(), dt)
        self.update_camera()

    def display(self):
        self.map_loader.collidable_tiles.clear()
        self.map_loader.killable_tiles.clear()
        self.map_loader.checkpoint_tiles.clear()
        self.screen.fill("#002904")

        self.map_loader.draw(target="Start", collidable=False, killable=False, screen=self.screen, camera_x=self.camera_x, camera_y=self.camera_y)
        self.map_loader.draw(target="Checkpoint", collidable=False, killable=False, screen=self.screen, camera_x=self.camera_x, camera_y=self.camera_y)
        self.map_loader.draw(target="Ground", collidable=True, killable=False, screen=self.screen, camera_x=self.camera_x, camera_y=self.camera_y)
        self.map_loader.draw(target="Top_spikes", collidable=False, killable=True, screen=self.screen, camera_x=self.camera_x, camera_y=self.camera_y)
        self.map_loader.draw(target="Left_spikes", collidable=False, killable=True, screen=self.screen, camera_x=self.camera_x, camera_y=self.camera_y)
        self.map_loader.draw(target="Right_spikes", collidable=False, killable=True, screen=self.screen, camera_x=self.camera_x, camera_y=self.camera_y)
        self.map_loader.draw(target="Bottom_spikes", collidable=False, killable=True, screen=self.screen, camera_x=self.camera_x, camera_y=self.camera_y)
        self.map_loader.draw(target="Props-3", collidable=False, killable=False, screen=self.screen, camera_x=self.camera_x, camera_y=self.camera_y)
        self.map_loader.draw(target="Props-2", collidable=False, killable=False, screen=self.screen, camera_x=self.camera_x, camera_y=self.camera_y)
        self.map_loader.draw(target="Props-1", collidable=False, killable=False, screen=self.screen, camera_x=self.camera_x, camera_y=self.camera_y)
        self.player. draw(screen=self.screen, camera_x=self.camera_x, camera_y=self.camera_y)
        self.map_loader.draw(target="Props+1", collidable=False, killable=False, screen=self.screen, camera_x=self.camera_x, camera_y=self.camera_y)
        
        if debug_mode:
            self.debug()
        pygame.display.flip()

    def run(self):
        FPS = 60  # Définir les FPS souhaités
        while self.running:
            # Limiter le framerate
            dt = self.clock.tick(FPS) / 1000.0  # Convertir en secondes
            
            self.handling_event()
            self.update()
            self.display()
    def debug(self):
        """Affiche les rectangles de debug avec le décalage caméra"""
        self.player.debug(self.screen, self.camera_x, self.camera_y)
        self.map_loader.debug(self.screen, self.camera_x, self.camera_y)

pygame.init()
pygame.display.set_caption("NameLess")
icon = pygame.image.load("../data/asset/images/logo.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

menu = main_menu(screen)
game = Game(screen)
game.run()
pygame.quit()
