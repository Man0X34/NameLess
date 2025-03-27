#Projet : NameLess
#Auteurs : Manoah Avril, Link Bernard, Noa Paté

import pygame

class Player:
    def __init__(self, x, y):
        self.sprite = pygame.image.load("../data/asset/images/character_sprite/idle/idle_0.png")
        self.speed = 160  # Vitesse en pixels par seconde
        self.velocity = [0, 0]  # Vitesse [X, Y]
        self.gravity = 700  # Gravité en pixels par seconde au carré
        self.max_fall_speed = 600  # Vitesse maximale de chute en pixels par seconde
        self.jump_strength = -400  # Force de saut en pixels par seconde
        self.on_ground = False  # Détection du sol

        self.sprite_width = 75
        self.sprite_height = 75
        self.checkpoint_tiles = []
        self.spawn = (x, y)  # Position de spawn
        self.facing_right = True
        self.direction = "R"  # Direction initiale
        self.last_direction = "R"  # Pour tracker les changements

        # Dimensions réduites pour le Rect
        hitbox_width = self.sprite_width * 0.5  # 50% de la largeur du sprite
        hitbox_height = self.sprite_height * 0.8  # 80% de la hauteur du sprite
        
        # Calculer les offsets pour centrer le rect
        offset_x = (self.sprite_width - hitbox_width) / 2
        offset_y = (self.sprite_height - hitbox_height) / 2 + 7

        # Créer un Rect centré
        self.rect = pygame.Rect(
            x,  # Position X sans décalage supplémentaire
            y,  # Position Y sans décalage supplémentaire
            hitbox_width,
            hitbox_height
        )

        # Stocker les offsets pour l'affichage
        self.display_offset_x = -offset_x
        self.display_offset_y = -offset_y
        
        # Variable d'images
        self.images = {
            "Idle": [
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/idle/idle_0.png"), (self.sprite_width, self.sprite_height)),
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/idle/idle_1.png"), (self.sprite_width, self.sprite_height)),
            ],
            "Idle2": [
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/idle2/idle2_0.png"), (self.sprite_width, self.sprite_height)),
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/idle2/idle2_1.png"), (self.sprite_width, self.sprite_height)),
            ],
            "Walk": [
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/walk/walk_0.png"), (self.sprite_width, self.sprite_height)),
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/walk/walk_1.png"), (self.sprite_width, self.sprite_height)),
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/walk/walk_2.png"), (self.sprite_width, self.sprite_height)),
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/walk/walk_3.png"), (self.sprite_width, self.sprite_height)),
            ],
            "JumpStart": [
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/jump/jump_0.png"), (self.sprite_width, self.sprite_height)),
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/jump/jump_1.png"), (self.sprite_width, self.sprite_height)),
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/jump/jump_2.png"), (self.sprite_width, self.sprite_height)),
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/jump/jump_3.png"), (self.sprite_width, self.sprite_height)),
            ],
            "JumpEnd": [
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/jump/jump_4.png"), (self.sprite_width, self.sprite_height)),
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/jump/jump_5.png"), (self.sprite_width, self.sprite_height)),
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/jump/jump_6.png"), (self.sprite_width, self.sprite_height)),
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/jump/jump_7.png"), (self.sprite_width, self.sprite_height)),
            ],
            "Glide": [
                pygame.transform.scale(pygame.image.load("../data/asset/images/character_sprite/jump/jump_4.png"), (self.sprite_width, self.sprite_height)),
            ],
        }

        self.image = self.images["Idle"][0]

        self.state = "Idle"
        self.frame = 0
        self.afk = 0


    def move(self, collidable_tiles, dt):
        """Déplace le joueur en fonction de la vélocité et gère les collisions avec le sol."""
        # Appliquer la gravité avec le temps
        if not self.on_ground:
            self.velocity[1] += self.gravity * dt
            if self.velocity[1] > self.max_fall_speed:
                self.velocity[1] = self.max_fall_speed

        # Déplacement horizontal avec le temps
        dx = self.velocity[0] * self.speed * dt
        self.rect.x += dx

        # Vérifier les collisions horizontales
        for tile, gid in collidable_tiles:
            if self.rect.colliderect(tile):
                if dx > 0:  # Se déplace vers la droite
                    self.rect.right = tile.left
                elif dx < 0:  # Se déplace vers la gauche
                    self.rect.left = tile.right

        # Déplacement vertical avec le temps
        dy = self.velocity[1] * dt
        self.rect.y += dy
        self.on_ground = False

        # Vérifier les collisions verticales
        for tile, gid in collidable_tiles:
            if self.rect.colliderect(tile):
                if dy > 0:  # Si le joueur tombe
                    self.rect.bottom = tile.top
                    self.on_ground = True
                    self.velocity[1] = 0
                elif dy < 0:  # Si le joueur saute
                    self.rect.top = tile.bottom
                    self.velocity[1] = 0

        # Vérification du sol
        ground_check = pygame.Rect(
            self.rect.x,
            self.rect.bottom,
            self.rect.width,
            2
        )
        
        for tile, gid in collidable_tiles:
            if ground_check.colliderect(tile):
                self.on_ground = True
                break

    def is_killed(self, killable_tiles):
        """Vérifie si le joueur entre en collision avec des tuiles mortelles."""
        for tile, gid in killable_tiles:
            if self.rect.colliderect(tile):
                self.go_to_checkpoint()
                return True
        return False

    def checkpoint_touched(self, checkpoint_tiles):
        """Vérifie si le joueur entre en collision avec des tuiles mortelles."""
        for tile, gid in checkpoint_tiles:
            if self.rect.colliderect(tile):
                if (tile.x, tile.y) not in self.checkpoint_tiles:
                    self.checkpoint_tiles.append((tile.x, tile.y))
                return True
        return False

    def update(self, collidable_tiles, killable_tiles, checkpoint_tiles, dt):
        """Met à jour l'état du joueur."""
        self.handle_input()  # Ajout de cette ligne
        self.move(collidable_tiles, dt)
        self.is_killed(killable_tiles)
        self.checkpoint_touched(checkpoint_tiles)
        self.manage_states()
        self.animate()
        if self.frame < 60:
            self.frame += 1
        else:
            self.frame = 0
        if self.state == "Idle" or self.state == "Idle2":
            self.afk += 1
        else:
            self.afk = 0

    def go_to_checkpoint(self):
        """Téléporte le joueur au dernier checkpoint rencontré."""
        if self.checkpoint_tiles:  # Vérifie si la liste n'est pas vide
            self.rect.x = self.checkpoint_tiles[-1][0]
            self.rect.y = self.checkpoint_tiles[-1][1]
        else:  # Si aucun checkpoint n'a été touché, retour au spawn
            self.rect.x = self.spawn[0]
            self.rect.y = self.spawn[1]
        
        self.velocity = [0, 0]
        self.on_ground = False

    def draw(self, screen, camera_x=0, camera_y=0):
        """Affiche le joueur sur l'écran."""
        # Position d'affichage ajustée avec la caméra
        display_x = self.rect.x - camera_x + self.display_offset_x
        display_y = self.rect.y - camera_y + self.display_offset_y
        screen.blit(self.image, (display_x, display_y))

    def handle_input(self):
        """Gestion des touches pour déplacer le joueur."""
        keys = pygame.key.get_pressed()
        self.velocity[0] = 0

        if keys[pygame.K_LEFT]:
            self.velocity[0] = -1
            self.direction = "L"
        elif keys[pygame.K_RIGHT]:
            self.velocity[0] = 1
            self.direction = "R"

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity[1] = self.jump_strength

    def debug(self ,screen, camera_x=0, camera_y=0):
        """DEBUG: Afficher la hitbox en rouge (ajustée avec la caméra)"""
        debug_rect = pygame.Rect(
            self.rect.x - camera_x,
            self.rect.y - camera_y,
            self.rect.width,
            self.rect.height
        )
        pygame.draw.rect(screen, (255, 0, 0), debug_rect, 2)
        print("Vélocité sur x : {}".format(self.velocity[0]))
        print("Vélocité sur y : {}".format(self.velocity[1]))
        print("On ground : {}".format(self.on_ground))
        print("State : {}".format(self.state))

    # ===============================================================================================================
    # Fonctions d'animations
    # à faire un jour peut-être
    # ===============================================================================================================

    def play_animation(self, animation, framerate):
        """Joue une animation avec la bonne direction."""
        frame_index = (self.frame // framerate) % len(self.images[animation])
        self.image = self.images[animation][frame_index]

        if self.direction == "L":
            self.image = pygame.transform.flip(self.image, True, False)

    def animate(self):
        """Joue les animations en fonction de 'state'."""
        if self.state == "Idle":
            self.play_animation("Idle", 30)
        elif self.state == "Idle2":
            self.play_animation("Idle2", 30)
        elif self.state == "Walk":
            self.play_animation("Walk", 10)
        elif self.state == "Jump":
            self.play_animation("Jump", 30)
        elif self.state == "Attack":
            self.play_animation("Attack", 30)
        elif self.state == "Sneak":
            self.play_animation("Sneak", 30)
        elif self.state == "FadeOut":
            self.play_animation("FadeOut", 30)
        elif self.state == "Glide":
            self.play_animation("Glide", 30)

    def manage_states(self):
        """Gère les changements d'état en fonction de la vélocité."""
        if self.velocity[0] == 0 and self.on_ground:
            if self.afk > 100:
                self.state = "Idle2"
            else:
                self.state = "Idle"
        elif self.velocity[0] != 0 and self.on_ground:
            self.state = "Walk"
        elif self.velocity[1] != 0:
            self.state = "Glide"
