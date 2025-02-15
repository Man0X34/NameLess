import pygame
from player import Player
from ground import Ground
from map_loader import MapLoader
import os

# Force le fichier à s'ouvrir dans "Jeu NSI"
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

    def handling_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.player.handle_input()

    def update(self):
        self.player.move(self.collidable_tiles)
        # self.player.animate_idle()   

    def display(self):
        self.screen.fill("white")

        # Affiche le joueur
        self.player.draw(self.screen)
        self.map_loader.draw(self.screen, offset_x=0, offset_y=0)

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
