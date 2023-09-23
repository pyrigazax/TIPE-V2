import pygame
import animation


class Player(animation.AnimateSprite):

    def __init__(self, x, y):
        super().__init__('player',"player_right")
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([255, 255, 255])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed = 1
        self.player_timer = 0
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 1)
        self.old_position = self.position.copy()
        self.save_position = self.position
        self.spawn_gostmode = 0
        self.gostmode = False
    
    def save_location(self): self.old_position = self.position.copy()

    def move_right(self):
        self.position[0] += self.speed
        self.image.set_colorkey([255, 255, 255])
        if self.player_timer == 5:
            self.player_timer = 0
        if self.player_timer == 0:
            self.start_animation()
            self.animate('player_right')
        self.player_timer += 1

    def move_left(self):
        self.position[0] -= self.speed
        self.image.set_colorkey([255, 255, 255])
        if self.player_timer == 5:
            self.player_timer = 0
        if self.player_timer == 0:
            self.start_animation()
            self.animate('player_left')
        self.player_timer += 1

    def move_up(self):
        self.position[1] -= self.speed
        self.image.set_colorkey([255, 255, 255])
        if self.player_timer == 5:
            self.player_timer = 0
        if self.player_timer == 0:
            self.start_animation()
            self.animate('player_up')
        self.player_timer += 1

    def move_down(self):
        self.position[1] += self.speed
        self.image.set_colorkey([255, 255, 255])
        if self.player_timer == 5:
            self.player_timer = 0
        if self.player_timer == 0:
            self.start_animation()
            self.animate('player_down')
        self.player_timer += 1

    def update_animation(self):
        self.image.set_colorkey([255, 255, 255])
        self.animate('player_down')
        
    def update(self):
        
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
    
    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface([4, 4])
        image.blit(self.image, (0, 0), (x, y, 4, 4))
        return image
