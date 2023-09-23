import pygame
import animation
from Visual_Coding import *

class Scientifique(animation.AnimateSprite):

    def __init__(self, x, y):
        super().__init__('scientifique',"pnj_right")
        self.sprite_sheet = pygame.image.load('scientifique/pnj_right1.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([255, 255, 255])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed = 1
        self.vc = None
        self.code = []
        self.read_actions = False
        self.read_stage = [0, 0] # the first number is the number of frames and the second
        # is the current instruction number
        self.scientifique_timer = 0
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.sight_range = 7 * 28
        self.sight_angle = 2 * 28
        self.direction = 'right'
    
    def save_location(self): self.old_position = self.position.copy()

    def move_right(self):
        self.position[0] += self.speed
        self.image.set_colorkey([255, 255, 255])
        if self.scientifique_timer == 5:
            self.scientifique_timer = 0
        if self.scientifique_timer == 0:
            self.start_animation()
            self.animate('scientifique_right')
        self.scientifique_timer += 1
        self.direction = 'right'

    def move_left(self):
        self.position[0] -= self.speed
        self.image.set_colorkey([255, 255, 255])
        if self.scientifique_timer == 5:
            self.scientifique_timer = 0
        if self.scientifique_timer == 0:
            self.start_animation()
            self.animate('scientifique_left')
        self.scientifique_timer += 1
        self.direction = 'left'

    def move_up(self):
        self.position[1] -= self.speed
        self.image.set_colorkey([255, 255, 255])
        if self.scientifique_timer == 5:
            self.scientifique_timer = 0
        if self.scientifique_timer == 0:
            self.start_animation()
            self.animate('scientifique_up')
        self.scientifique_timer += 1
        self.direction = 'up'

    def move_down(self):
        self.position[1] += self.speed
        self.image.set_colorkey([255, 255, 255])
        if self.scientifique_timer == 5:
            self.scientifique_timer = 0
        if self.scientifique_timer == 0:
            self.start_animation()
            self.animate('scientifique_down')
        self.scientifique_timer += 1
        self.direction = 'down'

    def update_animation(self):
        self.image.set_colorkey([255, 255, 255])
        self.animate('scientifique_down')
        
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
    
    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.image, (0, 0), (x, y, 32, 32))
        return image
    
    def code_actions(self):
        if self.vc == None:
            temp = pygame.Surface((0,0))
            block_list = {("Logique", (216,166,48)):[
                StartBlock((30, (216,166,48)), (115, 0), temp),
                Repete("Répéter  fois", (20, (41, 177, 35)), (50, 0), temp, 8, max_chars=9),
                While(" "*6 + "Tant que", (20, (41, 177, 35)), (75, 0), temp, w=200),
                BlockWithInput(" "*6 + "Condition:\n§", (20, (126,45,237)), (75, 0), temp, 27, w=200),
                IfElse(" "*6 + "Si:", (20, (41, 177, 35)), (75, 0), temp, w=200, start=2),
                IfElse(" "*6 + "Si:\n Sinon:", (20, (41, 177, 35)), (75, 0), temp, w=200, Else=True, start=2)],
                ("Var et aff", (135,62,35)):[
                BlockWithInputs("Créer la variable  avec la valeur ", (20, (170,58,21)), (50, 0), temp, (18, 34),
                                interlign_space=5),
                BlockWithInputs("Affecter l'opération  à la variable ", (20, (170,58,21)), (50, 0), temp, (21, 36),
                                interlign_space=5),
                BlockWithInput("Afficher ", (20, (170,58,21)), (50, 0), temp, 9)],
                ("Mvts", (14,62,236)): [
                BlockWithInput("Bouger de  bloc à droite", (20, (14,62,236)), (50, 0), temp, 10),
                BlockWithInput("Bouger de  bloc à gauche", (20, (14,62,236)), (50, 0), temp, 10),
                BlockWithInput("Bouger de  bloc vers le bas", (20, (14,62,236)), (50, 0), temp, 10),
                BlockWithInput("Bouger de  bloc vers le haut", (20, (14,62,236)), (50, 0), temp, 10)]
            }
            self.code, self.vc = init_visual_coding(block_list, self)
            self.translator = self.vc.translator
        else:
            self.vc.run()
            self.code = self.vc.code
