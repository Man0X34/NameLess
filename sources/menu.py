#-------------------------------------------------------------------------------
# Name:        main
# Purpose:     Crée l'écran de menu.
#
# Author:      Link
#
# Created:     28/03/2025
# Licence:     GPL v3+
#-------------------------------------------------------------------------------

import pygame 
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Fonction pour charger un fond
def load_background(image_path, screen):
    """Charge et affiche une image de fond redimensionnée à l'écran."""
    try:
        background = pygame.image.load(image_path)  # Charger l'image
        background = pygame.transform.scale(background, screen.get_size())  # Adapter à l'écran
        screen.blit(background, (0, 0))  # Dessiner le fond
    except pygame.error:
        print("⚠ Impossible de charger l'image de fond. Vérifiez le chemin du fichier.")

# Fonction pour charger l'image de l'encadré
def load_frame_image(screen, frame_path, box_x, box_y, box_width, box_height):
    """Charge et affiche une image d'encadré à la place du rectangle semi-transparent."""
    try:
        frame_image = pygame.image.load(frame_path)  # Charger l'image
        frame_image = pygame.transform.scale(frame_image, (box_width, box_height))  # Adapter à la taille voulue
        screen.blit(frame_image, (box_x, box_y))  # Appliquer sur l'écran
    except pygame.error:
        print("⚠ Impossible de charger l'image de l'encadré. Vérifiez le chemin du fichier.")

def main_menu(screen):
    """Affiche un menu interactif avec un encadré autour du titre et du bouton."""

   
    pygame.font.init()
    font = pygame.font.Font(None, 50)

 # Charger les images du bouton
    button_normal = pygame.image.load("../data/asset/Menu/play1.png")
    button_hovered = pygame.image.load("../data/asset/Menu/play3.png")

    keys_normal = pygame.image.load("../data/asset/Menu/keys1.png")
    keys_hovered = pygame.image.load("../data/asset/Menu/keys3.png")

    button_width, button_height = button_normal.get_size()
    keys_width, keys_height = keys_normal.get_size()

    running = True

    while running:
        screen.fill((0, 0, 0))
        load_background("../data/asset/Menu/background.png", screen)   ############ a changer plus tard avec image de la map avec ou sans le perso

        # Récupérer la taille de l'écran
        screen_width, screen_height = screen.get_size()

        # Définition des dimensions de l'encadré
        box_width, box_height = 500, 400
        box_x = (screen_width - box_width) / 2
        box_y = screen_height / 3 - 50

        # Charger et afficher l'image de l'encadré
        load_frame_image(screen, "../data/asset/Menu/scroll.png", box_x/3, box_y/5, box_width*2, box_height*2.25)

       #ORDRE DES BOUTONS
        keys_x = (screen_width - keys_width) / 2
        keys_y = box_y + 200  # Bouton "option" en haut

        button_x = (screen_width - button_width) / 2
        button_y = keys_y + keys_height + 50  # Bouton "Jouer" en dessous

        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered_play = (button_x <= mouse_x <= button_x + button_width) and (button_y <= mouse_y <= button_y + button_height)
        is_hovered_keys = (keys_x <= mouse_x <= keys_x + keys_width) and (keys_y <= mouse_y <= keys_y + keys_height)

        # Sélectionner l'image du bouton en fonction de l'état
        button_image = button_hovered if is_hovered_play else button_normal
        keys_image = keys_hovered if is_hovered_keys else keys_normal

        screen.blit(button_image, (button_x, button_y))
        screen.blit(keys_image, (keys_x, keys_y))

        # Dessiner le titre centré dans l'encadré
        title = font.render("NameLess", True, (0, 0, 0))
        title_rect = title.get_rect(center=(screen_width / 2, box_y + 90))
        screen.blit(title, title_rect)

       

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Échap pour quitter
                    running = False            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_hovered_play:
                    return "jouer"  # Lance le jeu
                if is_hovered_keys:
                    menu_touches(screen)  # Affiche directement le menu des touches

        pygame.display.flip()

def menu_touches(screen):
    """Affiche le menu des touches et permet de revenir au menu principal."""
    pygame.font.init()
    font = pygame.font.Font(None, 50)
    
    running = True
    while running:
        screen.fill((0, 0, 0))
        load_background("../data/asset/Menu/background.png", screen)   ############ a changer plus tard avec image de la map avec ou sans le perso

        # Récupérer la taille de l'écran
        screen_width, screen_height = screen.get_size()

        # Dimensions et position de l'encadré
        box_width, box_height = 600, 500
        box_x = (screen_width - box_width) / 2
        box_y = screen_height / 3 - 50

        # Charger l'image de fond de l'encadré (même image que le menu principal)
        box_background = pygame.image.load("../data/asset/Menu/scroll 2.png")
        box_background = pygame.transform.scale(box_background, (box_width, box_height))

        # Dessiner l'image de fond pour l'encadré
        screen.blit(box_background, (box_x, box_y))

        

        # Titre du menu des touches
        title = font.render("keys bind", True, (0, 0, 0))
        title_rect = title.get_rect(center=(screen_width / 2, box_y + 90))
        screen.blit(title, title_rect)

        # Charger les images des touches
        key_left_image = pygame.image.load("../data/asset/Menu/gauche.png")  # Image pour aller à gauche
        key_right_image = pygame.image.load("../data/asset/Menu/droite.png")  # Image pour aller à droite
        key_space_image = pygame.image.load("../data/asset/Menu/space.png")  # Image pour sauter

        # Agrandir les images x3 pour une meilleure visibilité
        scale_factor = 3
        key_left_image = pygame.transform.scale(key_left_image, (key_left_image.get_width() * scale_factor, key_left_image.get_height() * scale_factor))
        key_right_image = pygame.transform.scale(key_right_image, (key_right_image.get_width() * scale_factor, key_right_image.get_height() * scale_factor))
        key_space_image = pygame.transform.scale(key_space_image, (key_space_image.get_width() * scale_factor, key_space_image.get_height() * scale_factor))

        key_width, key_height = key_left_image.get_size()
        

        # Position des éléments dans l'encadré
        start_x = box_x + 220  # Position du texte (décalé à droite de l'image)
        image_x = start_x - key_width - 20  # Décaler l'image à gauche du texte
        y_position = box_y + 150  # Position verticale initiale

       
       
        # Affichage des touches
        screen.blit(key_left_image, (image_x, y_position))
        label_left = font.render("go left", True, (0, 0, 0))
        screen.blit(label_left, (start_x, y_position + key_height / 2 - label_left.get_height() / 2))

        y_position += key_height + 30

        screen.blit(key_right_image, (image_x, y_position))
        label_right = font.render("go right", True, (0, 0, 0))
        screen.blit(label_right, (start_x , y_position + key_height / 2 - label_right.get_height() / 2))

        y_position += key_height + 30

        screen.blit(key_space_image, (image_x, y_position))
        label_space = font.render("jump", True, (0, 0, 0))
        screen.blit(label_space, (start_x +60, y_position + key_height / 2 - label_space.get_height() / 2))

        # Bouton "Retour"
        button_normal = pygame.image.load("../data/asset/Menu/back1.png")
        button_hovered = pygame.image.load("../data/asset/Menu/back3.png")
        
        scale_factor = 2.5  # Facteur d'agrandissement

        button_normal = pygame.transform.scale(button_normal, (button_normal.get_width() * scale_factor, button_normal.get_height() * scale_factor))
        button_hovered = pygame.transform.scale(button_hovered, (button_hovered.get_width() * scale_factor, button_hovered.get_height() * scale_factor))

        
        button_width, button_height = button_normal.get_size()
        button_x = (screen_width - button_width) / 2
        button_y = box_y + box_height - 150

        # Vérifier si la souris est sur le bouton
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered = (button_x <= mouse_x <= button_x + button_width) and (button_y <= mouse_y <= button_y + button_height)

        # Sélectionner l'image du bouton en fonction de l'état
        button_image = button_hovered if is_hovered else button_normal
        screen.blit(button_image, (button_x, button_y))

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_hovered:
                    return  # Retour au menu principal

        pygame.display.flip()


def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    
    main_menu(screen)  # Afficher le menu avant de lancer le jeu
    
    running = True
    while running:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
