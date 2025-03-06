import pygame

class Player:
    def __init__(self, x, y):
        self.sprite = pygame.image.load("asset/character_sprite/idle/idle_0.png")
        self.speed = 5
        self.velocity = [0, 0]  # Vitesse [X, Y]
        self.gravity = 0.5  # Gravité appliquée au joueur
        self.max_fall_speed = 10  # Vitesse maximale de chute
        self.jump_strength = -10  # Puissance du saut
        self.on_ground = False  # Détection du sol

        self.sprite_width = 80
        self.sprite_height = 80

        # Redimensionner l'image
        self.image = pygame.transform.scale(self.sprite, (self.sprite_width, self.sprite_height))

        # Dimensions réduites pour le Rect
        hitbox_width = self.sprite_width * 0.5  # 50% de la largeur du sprite
        hitbox_height = self.sprite_height * 0.8  # 80% de la hauteur du sprite
        
        # Calculer les offsets pour centrer le rect
        offset_x = (self.sprite_width - hitbox_width) / 2
        offset_y = (self.sprite_height - hitbox_height) / 2

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

    def apply_gravity(self):
        """Applique la gravité si le joueur est en l'air."""
        if not self.on_ground:
            self.velocity[1] += self.gravity
            if self.velocity[1] > self.max_fall_speed:
                self.velocity[1] = self.max_fall_speed

    def move(self, collidable_tiles):
        """Déplace le joueur en fonction de la vélocité et gère les collisions avec le sol."""
        self.apply_gravity()  # Appliquer la gravité

        # Déplacement horizontal
        self.rect.x += self.velocity[0] * self.speed

        # Vérifier les collisions horizontales
        for tile in collidable_tiles:
            if self.rect.colliderect(tile):
                if self.velocity[0] > 0:  # Se déplace vers la droite
                    self.rect.right = tile.left
                elif self.velocity[0] < 0:  # Se déplace vers la gauche
                    self.rect.left = tile.right

        # Déplacement vertical
        self.rect.y += self.velocity[1]
        self.on_ground = False  # Supposer qu'il est en l'air par défaut

        # Vérifier les collisions verticales
        for tile in collidable_tiles:
            if self.rect.colliderect(tile):
                if self.velocity[1] > 0:  # Si le joueur tombe
                    self.rect.bottom = tile.top
                    self.on_ground = True
                    self.velocity[1] = 0
                elif self.velocity[1] < 0:  # Si le joueur saute
                    self.rect.top = tile.bottom
                    self.velocity[1] = 0

    def draw(self, screen, camera_x=0, camera_y=0):
        """Affiche le joueur sur l'écran."""
        # Position d'affichage ajustée avec la caméra
        display_x = self.rect.x - camera_x + self.display_offset_x
        display_y = self.rect.y - camera_y + self.display_offset_y
        screen.blit(self.image, (display_x, display_y))
        
        # DEBUG: Afficher la hitbox en rouge (ajustée avec la caméra)
        debug_rect = pygame.Rect(
            self.rect.x - camera_x,
            self.rect.y - camera_y,
            self.rect.width,
            self.rect.height
        )
        pygame.draw.rect(screen, (255, 0, 0), debug_rect, 2)

    def handle_input(self):
        """Gestion des touches pour déplacer le joueur."""
        keys = pygame.key.get_pressed()

        # Réinitialisation des mouvements
        self.velocity[0] = 0  

        if keys[pygame.K_LEFT] or keys[pygame.K_LEFT]:
            self.velocity[0] = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_RIGHT]:
            self.velocity[0] = 1

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity[1] = self.jump_strength  # Appliquer la force de saut

    # ===============================================================================================================
    # Fonctions d'animations
    # ===============================================================================================================

    def animate_idle(self):
        frame_rate = 30
        for frame in range(2):
            original_image = pygame.image.load(f"asset/character_sprite/idle/idle_{frame}.png")
            self.image = pygame.transform.scale(original_image, (self.sprite_width, self.sprite_height))
            pygame.time.delay(frame_rate)
    def animate_idle2(self):
        pass
    def animate_walk(self):
        pass
    def animate_jump(self):
        pass
    def animate_attack(self):
        pass
    def animate_sneak(self):
        pass
    def animate_fade_out(self):
        pass
    def animate_sleep(self):
        pass
    def animate_run(self):
        pass
