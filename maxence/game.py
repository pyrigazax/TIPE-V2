import pygame
import pytmx
import pyscroll
from random import randint

from player import Player
from scientifique import Scientifique



class Game:

    def __init__(self):
        # creation de la fenetre de jeu
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("TIPE_Maxence")

        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('carte_ascent.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.zoom = map_layer.zoom = 1.2
        self.map = 'carte_ascent'
        self.frame = 0

        # generer un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)


        # definir une liste qui stock les rectangles de collisision
        self.walls = []

        for obj in tmx_data.objects : 
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)
        

        # definir le rect de collision pour entrer dans la maison
        exit_world = tmx_data.get_object_by_name('enter_start_house')
        self.exit_world_rect = pygame.Rect(exit_world.x, exit_world.y, exit_world.width, exit_world.height)

        exit_world_1 = tmx_data.get_object_by_name('enter_tuto_1')
        self.exit_world_1_rect = pygame.Rect(exit_world_1.x, exit_world_1.y, exit_world_1.width, exit_world_1.height)

    
    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_z]:
            self.player.move_up()
            
        elif pressed[pygame.K_s]:
            self.player.move_down()
            
        elif pressed[pygame.K_q]:
            self.player.move_left()

        elif pressed[pygame.K_d]:
            self.player.move_right()

    def ghost_mod(self, event):
        pressed = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.player.save_position = self.player.position.copy()
            self.player.gostmode = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE: 
            self.player.position = self.player.save_position
            self.player.gostmode = False


    def pnj_mouvement(self):
        self.scientifique.move_left()
        self.scientifique_1.move_down()
        self.scientifique_2.move_up()
        self.scientifique_3.move_right()
        self.scientifique_4.move_left()
        self.scientifique_5.move_left()
        self.scientifique_6.move_left()

        
 
    def control_pnj(self, pnj):
        if pnj.code != []:
            a = pnj.translator.execute_npc(pnj)
            if a:
                self.scientifique.read_actions = False
        else:
            self.scientifique.read_actions = False
    
    def spawn(self,id):
        id_position = pytmx.util_pygame.load_pygame('carte_ascent.tmx').get_object_by_name(id)
        self.id = Scientifique(id_position.x, id_position.y)
        self.group.add(self.id)
        return self.id


        

    def switch_world(self, world, other_world, two_liasons, liason_2, spawn, zoom):
        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame(other_world + '.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = zoom
        self.map = other_world
        

        # definir une liste qui stock les rectangles de collisision
        self.walls = []

        for obj in tmx_data.objects : 
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer = 5)
        self.group.add(self.player)

        # definir le rect de collision pour sortir du monde
        exit_world = tmx_data.get_object_by_name('enter_'+ world)
        self.exit_world_rect = pygame.Rect(exit_world.x, exit_world.y, exit_world.width, exit_world.height)
        if two_liasons:
            exit_world_1 = tmx_data.get_object_by_name('enter_'+ liason_2)
            self.exit_world_1_rect = pygame.Rect(exit_world_1.x, exit_world_1.y, exit_world_1.width, exit_world_1.height)

        # definir le système de porte
        if other_world == 'level-1':
            porte = tmx_data.get_object_by_name('porte_1')
            self.porte_rect = pygame.Rect(porte.x, porte.y, porte.width, porte.height)
            interrupteur = tmx_data.get_object_by_name('interrupteur_porte')
            self.interrupteur_rect = pygame.Rect(interrupteur.x, interrupteur.y, interrupteur.width, interrupteur.height)

        
        

        # recuperer le point de spawn devans la maison
        spawn_house_point = tmx_data.get_object_by_name('spawn_' + spawn)
        self.player.position[0] = spawn_house_point.x - 10
        self.player.position[1] = spawn_house_point.y - 20

    def game_over_verification(self, id_mob):
        
        if self.map == 'carte_ascent':
            
            if id_mob.direction == 'right':
                if id_mob.position[0] < self.player.position[0] < id_mob.position[0] + id_mob.sight_range:
                    if id_mob.position[1] - id_mob.sight_angle < self.player.position[1] < id_mob.position[1] + id_mob.sight_angle:
                        for obj in pytmx.util_pygame.load_pygame('carte_ascent.tmx').objects:
                            print(f'{id_mob.position[0]} < {obj.x} < {self.player.position[1]}', obj.y , id_mob.position[1])
                            if obj.type == 'collision' and id_mob.position[0] < obj.x < self.player.position[1] and (obj.y - (obj.h)/2) < id_mob.position[1] (obj.y + (obj.h)/2): print('2')
                            else: None
                            
            elif id_mob.direction == 'left':
                if id_mob.position[0] - id_mob.sight_range < self.player.position[0] < id_mob.position[0]:
                    if id_mob.position[1] - id_mob.sight_angle < self.player.position[1] < id_mob.position[1] + id_mob.sight_angle:
                        for obj in pytmx.util_pygame.load_pygame('carte_ascent.tmx').objects:
                            if obj.type == 'collision' and id_mob.position[0] - id_mob.sight_range < obj.x < id_mob.position[0] and obj.y == id_mob.position[1]: print('2')
                            else: None

            elif id_mob.direction == 'up':
                if id_mob.position[0] - id_mob.sight_angle < self.player.position[0] < id_mob.position[0] + id_mob.sight_angle:
                    if not(id_mob.position[1] > self.player.position[1] > (id_mob.position[1] + id_mob.sight_range)):
                        for obj in pytmx.util_pygame.load_pygame('carte_ascent.tmx').objects:
                            if obj.type == 'collision' and not(id_mob.position[1] > self.player.position[1] > (id_mob.position[1] + id_mob.sight_range)) and obj.x == id_mob.position[0]: print('2')
                            else: None

            elif id_mob.direction == 'down':
                if id_mob.position[0] - id_mob.sight_angle < self.player.position[0] < id_mob.position[0] + id_mob.sight_angle:
                    if not(id_mob.position[1] - id_mob.sight_range < self.player.position[1] < id_mob.position[1]):
                        for obj in pytmx.util_pygame.load_pygame('carte_ascent.tmx').objects:
                            if obj.type == 'collision' and not(id_mob.position[1] - id_mob.sight_range < self.player.position[1] < id_mob.position[1]) and obj.x == id_mob.position[0]: print('2')
                            else: None

    def update(self):
        self.group.update()

        # verifier l'entrer dans le level 1
        if self.map == 'carte_ascent' and self.player.feet.colliderect(self.exit_world_1_rect):
            # generer les pnj
            self.scientifique_A1 = self.spawn('scientifique_A1')
            self.scientifique_A2 = self.spawn('scientifique_A2')
            self.scientifique_A3 = self.spawn('scientifique_A3')
            self.scientifique_A4 = self.spawn('scientifique_A4')
            self.scientifique_A5 = self.spawn('scientifique_A5')
            self.scientifique_D1 = self.spawn('scientifique_D1')
            self.scientifique_D2 = self.spawn('scientifique_D2')
            self.scientifique_D3 = self.spawn('scientifique_D3')
            self.scientifique_D4 = self.spawn('scientifique_D4')
            self.scientifique_D5 = self.spawn('scientifique_D5')
            self.scientifiques = [self.scientifique_A1, self.scientifique_A2 , self.scientifique_A3 , self.scientifique_A4 , self.scientifique_A5 , self.scientifique_D1, self.scientifique_D2 , self.scientifique_D3 , self.scientifique_D4 , self.scientifique_D5 ]

        # verifier collision porte
        for sprite in self.group.sprites():
            if self.map == 'level-1' and self.player.feet.colliderect(self.porte_rect) and self.player.gostmode == False:
                if self.scientifique.feet.colliderect(self.interrupteur_rect) == False:
                    sprite.move_back()

        # verification collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1 and self.player.gostmode == False:
                sprite.move_back()
            if sprite != self.player and sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()
        
        # verification game over
        if self.map == 'level-1':
            for scientifique in self.scientifiques:
                self.game_over_verification(scientifique)
    
    def rect_scientifique(self, id):
        id.rect.y = id.position[1] * self.zoom
        id.rect.x = id.position[0] * self.zoom
        id.rect.w = 32 * self.zoom
        id.rect.h = 32 * self.zoom
        if self.player.position[0] > 195:
            id.rect.x =  id.rect.x - (self.player.position[0] - 195) *3 
        if self.player.position[1] > 105:
            id.rect.y =  id.rect.y - (self.player.position[1] - 105) *3 
   
    def run(self):

        clock = pygame.time.Clock()

        # boucle du jeu
        game_running = True

        while game_running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                if event.type == pygame.MOUSEBUTTONDOWN and self.map == 'level-1':
                    if self.scientifique.rect.collidepoint(event.pos):
                        if event.button == 1:
                            self.scientifique.code_actions()
                        elif event.button == 3:
                            self.scientifique.read_stage = [0, 0]
                            self.scientifique.read_actions = True
                self.ghost_mod(event)

            self.player.save_location()
            if self.map == 'level-1':
                self.scientifique.save_location()
                if self.scientifique.read_actions:
                    self.control_pnj(self.scientifique)
                elif 800 < self.frame  < 810: 
                    self.pnj_mouvement()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            if self.map == 'level-1':
                for scientifique in self.scientifiques :
                    self.rect_scientifique(scientifique)
            pygame.display.flip()
            self.frame += 1 
            clock.tick(60)

        pygame.quit()
