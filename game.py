import pygame
from player import Player
from ground import Ground
from map_loader import MapLoader
import os

# Force le fichier à s'ouvrir dans "Jeu NSI (car sinon il s'ouvre n'importe où et ne trouve aps les fichiers)
os.chdir(r"C:\Users\Manoah Avril\Desktop\Fichier\Programmation\Jeu NSI")

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.player = Player(100, 100)  # Position de départ du joueur

        self.map_loader = MapLoader()

        # Liste des plateformes (sols)
        self.collidable_tiles = self.map_loader.get_collidable_tiles()

        self.camera_x = 0
        self.camera_y = 0

    def handling_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.player.handle_input()

    def update_camera(self):
        # Obtenir les dimensions de l'écran
        screen_width, screen_height = self.screen.get_size()
        
        # Centrer la caméra sur le joueur
        target_x = self.player.rect.centerx - screen_width // 2
        target_y = self.player.rect.centery - screen_height // 2
        
        # Limites de la carte
        max_camera_x = self.map_loader.map_width - screen_width
        max_camera_y = 0
        
        # Appliquer les limites
        self.camera_x = max(0, min(target_x, max_camera_x))
        self.camera_y = max(0, min(target_y, max_camera_y))

    def update(self):
        self.player.move(self.collidable_tiles)
        # self.player.animate_idle()
        self.update_camera()

    def display(self):
        self.screen.fill("white")
        self.map_loader.draw(self.screen, self.camera_x, self.camera_y)
        self.player.draw(self.screen, self.camera_x, self.camera_y)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handling_event()
            self.update()
            self.display()
            self.clock.tick(60)

pygame.init()
screen = pygame.display.set_mode((1300, 900))
game = Game(screen)
game.run()
pygame.quit()
