import pygame

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("asset/character_sprite/idle/idle_0.png")
        self.speed = 5
        self.velocity = [0, 0]  # Vitesse [X, Y]
        self.gravity = 0.5  # Gravité appliquée au joueur
        self.max_fall_speed = 10  # Vitesse maximale de chute
        self.jump_strength = -10  # Puissance du saut
        self.on_ground = False  # Détection du sol

        # Dimensions réduites pour le Rect
        reduced_width = self.image.get_width() - 14  # Ajustez selon vos besoins
        reduced_height = self.image.get_height() - 14  # Ajustez selon vos besoins
        
        # Décalage du Rect
        offset_x = -7  # Décalage horizontal
        offset_y = -7  # Décalage vertical

        # Créer un Rect plus petit
        self.rect = pygame.Rect(x+offset_x, y+offset_y, reduced_width, reduced_height)

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

    def draw(self, screen):
        """Affiche le joueur sur l'écran."""
        screen.blit(self.image, self.rect)

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
            self.image = pygame.image.load(f"asset/character_sprite/idle/idle_{frame}.png")
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