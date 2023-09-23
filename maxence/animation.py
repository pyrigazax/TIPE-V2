import pygame

# definir une classe qui s'occupe des animations
class AnimateSprite(pygame.sprite.Sprite):

    # définir les mouvements des entitées
    def __init__(self, folder_name, sprite_name):
        super().__init__()
        self.image = pygame.image.load(f'{folder_name}/{sprite_name}1.png')
        self.image.set_colorkey([255, 255, 255])
        self.current_image = 0 # commencer l'animation à l'image 0
        self.images = animations.get(sprite_name)
        self.animation = False

    #définir une methode pour demarrer l'animation
    def start_animation(self):
        self.animation = True

    # definir une methode pour animer le sprite
    def animate(self,sprite_name):
        self.image.set_colorkey([255, 255, 255])
        #verifier si l'animation est active
        self.images = animations.get(sprite_name)

        if self.animation:

            # passer à l'image suivante
            self.current_image += 1
            
            # verifier si on atteint la fin de l'animation
            if self.current_image >= len(self.images):
                # remettre l'anim à 0
                self.current_image = 0
                #désactivation de l'animation
                self.animation = False
            
            # modifier l'image précédente par la suivante
            self.image = self.images[self.current_image]

# definir une fonction pour charger les images d'un sprite
def load_animation_images(folder_name, sprite_name):
    # charge les images de ce sprite dans le dossier correspondant
    images = []
    
    path = f"{folder_name}/{sprite_name}"
    # boucler sur chaque image du perso
    for num in range(1,4):
            image_path = path + str(num) + '.png'
            print(image_path)
            images.append(pygame.image.load(image_path))
    return images


# definir un dictionnaire qui va contenir les images chargées de chaque sprite
animations = {
    'player_down': load_animation_images('player', 'player_down'),
    'player_left': load_animation_images('player', 'player_left'),
    'player_right': load_animation_images('player', 'player_right'),
    'player_up': load_animation_images('player', 'player_up'),
    'pnj_down': load_animation_images('scientifique', 'pnj_down'),
    'pnj_left': load_animation_images('scientifique', 'pnj_left'),
    'pnj_right': load_animation_images('scientifique', 'pnj_right'),
    'pnj_up': load_animation_images('scientifique', 'pnj_up')
}
