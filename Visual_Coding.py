import pygame
import sys
sys.path.append(r'C:\Users\gaeta\Documents\Gaétan_back_up_13.04.2021\Ecole\NSI\Projet_insider')
try:
    from Projet_insider.Blocks import *
    from Projet_insider.Transcription_python import *
except:
    from Blocks import *
    from Transcription_python import *
pygame.init()


class Menu:
    def __init__(self, screen, window):
        self.screen = screen
        self.window = window
        self.hidden = False
        self.menu_area = pygame.Surface((400, screen.get_height()))
        self.height = self.menu_area.get_height()
        self.deleted = False
        self.top = 0
        self.auto_link = False
        self.auto_link_rect = pygame.Rect((280, self.height-15), (10, 10))
        self.show_hide_rect = pygame.Rect((400,7), (40,40))

    def create_blocklist(self, block_list):
        self.menus_list = [list(i) for i in block_list.keys()]
        y = 10
        for menu in self.menus_list:
            height = blit_text(pygame.Surface((65, 50)), menu[0], (5, 0),
                               pygame.font.SysFont("Arial", 16))[0]
            menu[0] = (pygame.Rect((0, y), (70, height)),
                       pygame.Surface((65, height)),
                       menu[0])
            y += height
        self.menus_rect = pygame.Rect((0, 0), (80, y+10))
        self.menus_list[0][0][0].w += 5
        self.large_block_list = block_list
        self.update_blocklist(list(self.large_block_list.values())[0])

    def update_blocklist(self, block_list):
        self.block_list = block_list.copy()
        self.block_list[0] = (self.block_list[0], 50)
        for i in range(1, len(self.block_list)):
            self.block_list[i] = (self.block_list[i], self.block_list[i-1][1]\
                + self.block_list[i-1][0].block.h + 50)
        for block in self.block_list:
            block[0].in_menu = True
            block[0].window = self.window
            block[0].set_menu(self)
            block[0].set_screen(self.screen)
        self.scroll_bar = ScrollBar(self.menu_area, (self.menu_area.get_width() - 15,10),
                (10, self.height - 40), self.height,
                self.block_list[-1][1] + self.block_list[-1][0].block.h + 40)
    
    def update(self):
        self.top = self.scroll_bar.update()
        for block in self.block_list:
            block[0].block.y = block[1] - self.top
            if block[0].block.y <= self.menus_rect.h + 5:
                if block[0].block.x < 87:
                    block[0].x_save = block[0].block.x
                    block[0].block.x = 87
            elif block[0].block.x == 87:
                block[0].block.x = block[0].x_save
            block[0].update()
        if self.hidden:
            self.show_hide_rect.x = 0
        else:
            self.show_hide_rect.x = 400

    def handle_event(self, event):
        self.scroll_bar.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for ind, menu in enumerate(self.menus_list):
                if menu[0][0].collidepoint(event.pos) and menu[0][0].w == 70:
                    self.update_blocklist(list(self.large_block_list.values())[ind])
                    menu[0][0].w += 5
                    for menu_bis in self.menus_list:
                        if menu_bis != menu:
                            menu_bis[0][0].w = 70
            
            if self.auto_link_rect.collidepoint(event.pos) or event.button == 2:
                self.auto_link = not self.auto_link

            if pygame.mouse.get_pos()[0] < 400 and not self.hidden:
                if event.button == 4:
                    if self.top > 0:
                        self.top -= 25
                        self.scroll_bar.set_value(self.top)
                elif event.button == 5:
                    if self.block_list[-1][1] + self.block_list[-1][0].block.h - self.height > self.top - 40:
                        self.top += 25
                        self.scroll_bar.set_value(self.top)

            elif self.show_hide_rect.collidepoint(event.pos):
                self.hidden = not self.hidden
                if self.hidden:
                    self.window.pos_indicator = ScrollRect(self.screen, (self.screen.get_width() - 85,
                                                    self.screen.get_height() - 85), (75, 75),
                                        (self.screen.get_width(), self.screen.get_height()),
                                        (self.screen.get_width()*3, self.screen.get_height()*3))
                    self.window.move_coding_area((0,0)) # updates the coding_area_pos
                    if self.window.coding_area_pos[0] <= 0:
                        save = self.window.coding_area_pos[0]
                        self.window.coding_area_pos[0] = 0
                        for obj in self.window.objects[2:]:
                            obj.update_pos((save, 0))
                else:
                    self.window.pos_indicator = ScrollRect(self.screen, (self.screen.get_width() - 85,
                                                    self.screen.get_height() - 85), (75, 75),
                                        (self.screen.get_width()-400, self.screen.get_height()),
                                        (self.screen.get_width()*3, self.screen.get_height()*3))
                    self.window.move_coding_area((0,0)) # updates the coding_area_pos
        for block in self.block_list:
            if block[1] > self.top - 200 and block[1] < self.top + self.height + 200 and not self.hidden:
                block[0].handle_event(event)
                
    def draw(self):
        pygame.draw.rect(self.screen, (0,0,0), self.show_hide_rect, border_top_right_radius=5,
                         border_bottom_right_radius=5)
        if not self.hidden:
            self.menu_area.fill((20,20,20))
            self.scroll_bar.draw()
            pygame.draw.lines(self.screen, (255,255,255), False, [(428,16), (411,27), (428, 38)], 5)
            for block in self.block_list:
                if block[1] > self.top - 200 and block[1] < self.top + self.height + 200:
                    block[0].draw()
            pygame.draw.rect(self.menu_area, (25,25,25), self.menus_rect,  border_bottom_right_radius=4)
            for menu in self.menus_list:
                pygame.draw.rect(self.menu_area, menu[1], menu[0][0], border_top_right_radius=2,
                         border_bottom_right_radius=2)
                menu[0][1].fill(menu[1])
                blit_text(menu[0][1], menu[0][2], (5, 0), pygame.font.SysFont("Arial", 16))
                self.menu_area.blit(menu[0][1], (menu[0][0].x, menu[0][0].y))
            pygame.draw.rect(self.menu_area, (25,25,25),
                             [0, self.menu_area.get_height()-25, self.menu_area.get_width(), 25], 0)
            blit_text(self.menu_area, "Lier automatiquement les 2 derniers blocs créés",
                      (5, self.menu_area.get_height()-20), pygame.font.SysFont("Arial", 15),
                      (255,255,255))
            pygame.draw.rect(self.menu_area, (255,255,255), self.auto_link_rect, 1)
            if self.auto_link:
                pygame.draw.rect(self.menu_area, (255,255,255),
                                 [282, self.menu_area.get_height()-13, 6, 6], 0)
            self.screen.blit(self.menu_area, (0, 0))
        else:
            pygame.draw.lines(self.screen, (255,255,255), False, [(11,16), (28,27), (11, 38)], 5)


class Console:
    def __init__(self, screen, w=350, h=None):
        self.screen = screen
        self.hidden = True
        self.console_color = (10,10,10)
        self.width = w
        if h == None:
            self.height = self.screen.get_height()/2-5
        else:
            self.height = h
        self.console_area = pygame.Surface((self.width, self.height))
        self.console_rect = pygame.Rect((self.screen.get_width()-w, screen.get_height()-self.height-5),
                                        (self.width, self.height+5))
        self.title_font = pygame.font.SysFont("Consolas", 30)
        self.title_w, self.title_h = self.title_font.size("Console:")
        self.text_console_area = pygame.Surface((self.console_area.get_width(),
                                                 self.console_area.get_height()-self.title_h-15))
        self.deleted = False
        self.top = 0
        self.console_text = ""
        self.show_hide_rect = pygame.Rect((self.screen.get_width()-30,
                                           self.screen.get_height()-self.height+100),
                                          (30,self.height-200))
        self.show_hide_text = FONT.render("Console", 0, (255,255,255))
        self.show_hide_text = pygame.transform.rotate(self.show_hide_text, 90)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.console_rect.collidepoint(event.pos) and not self.hidden:
                if event.button == 4:
                    if self.top > 0:
                        self.top -= 15
                elif event.button == 5:
                    if self.text_height >= self.text_console_area.get_height() + self.top:
                        self.top += 15
            if self.show_hide_rect.collidepoint(pygame.mouse.get_pos()):
                self.hidden = not self.hidden
    
    def log_console(self, text, end_line=True):
        self.console_text += text
        if end_line:
            self.console_text += "\n"
        else:
            self.console_text += " "
        if self.hidden:
            self.hidden = False
    
    def update(self):
        if self.hidden:
            self.show_hide_rect.x = self.screen.get_width() - self.show_hide_rect.w
        else:
            self.show_hide_rect.x = self.screen.get_width() - self.show_hide_rect.w - self.width
    
    def draw(self):
        # we draw first the show_hide button:
        pygame.draw.rect(self.screen, self.console_color, self.show_hide_rect, border_top_left_radius=3,
                         border_bottom_left_radius=3)
        self.screen.blit(self.show_hide_text, (self.show_hide_rect.x,
                        self.show_hide_rect.y+(self.show_hide_rect.h-self.show_hide_text.get_height())/2))
        # arrows
        if not self.hidden:
            pygame.draw.rect(self.screen, self.console_color, self.console_rect, border_top_left_radius=5)
            self.console_area.fill(self.console_color)
            blit_text(self.console_area, "Console:",((self.console_area.get_width() - self.title_w)/2, 10),
                      self.title_font, (255,255,255))
            self.text_console_area.fill(self.console_color)
            self.text_height = blit_text(self.text_console_area, self.console_text, (5, -self.top),
                    pygame.font.SysFont("Consolas", 15), (255,255,255))[0]
            self.console_area.blit(self.text_console_area, (0, self.title_h+15))
            self.screen.blit(self.console_area,
                            (self.screen.get_width()-self.width, self.screen.get_height()-self.height))
        


class VisualCoding:
    def __init__(self, screen):
        self.screen = screen
        self.coding_area_pos = [-400, 0]
        self.code = []
        self.clock = pygame.time.Clock() # self.objects at the beginning of the frame
        self.objects = []
        self.console = None
        self.block_moving = False
        self.translator = Translator()
        self.activated_anchor = None
        self.links_list = []
        self.read_code_rect = pygame.Rect((self.screen.get_width()-150, 0),
                                          (150, 35))
        self.validate_rect = pygame.Rect((self.screen.get_width()-120, 35),
                                          (120, 35))
        self.pos_indicator = ScrollRect(self.screen, (self.screen.get_width() - 85,
                                                      self.screen.get_height() - 85), (75, 75),
                                        (self.screen.get_width()-400, self.screen.get_height()),
                                        (self.screen.get_width()*3, self.screen.get_height()*3))
    
    def add_widgets(self, menu, console):
        self.objects.append(menu)
        self.objects.append(console)
        self.console = console

    def handling_events(self):
        self.objects_save = self.objects.copy() # we do this here because it's the first instruction of the main loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mouse.get_rel()
                if self.read_code_rect.collidepoint(event.pos):
                    self.read_code()
                    if self.code != None:
                        self.run_code()
                elif self.validate_rect.collidepoint(event.pos):
                    a = self.read_code()
                    if self.code != None:
                        b = self.run_code()
                    else:
                        b = "Erreur"
                    if a == None and b == None:
                        self.running = False
            for obj in self.objects:
                obj.handle_event(event)
    
    def move_coding_area(self, mouse_velo):
        for i in range(len(mouse_velo)):
            self.coding_area_pos[i] += -mouse_velo[i]
        mini = -400*(not self.objects[0].hidden)
        if mini <= self.coding_area_pos[0] <= self.screen.get_width() * 2 and\
          0 <= self.coding_area_pos[1] <= self.screen.get_height() * 2:
            for obj in self.objects[2:]:
                obj.update_pos(mouse_velo)
        elif mini <= self.coding_area_pos[0] <= self.screen.get_width() * 2:
            self.coding_area_pos[1] -= -mouse_velo[1]
            for obj in self.objects[2:]:
                obj.update_pos((mouse_velo[0], 0))
        elif 0 <= self.coding_area_pos[1] <= self.screen.get_height() * 2:
            self.coding_area_pos[0] -= -mouse_velo[0]
            for obj in self.objects[2:]:
                obj.update_pos((0, mouse_velo[1]))
        else:
            for i in range(len(mouse_velo)):
                self.coding_area_pos[i] -= -mouse_velo[i]
        self.pos_indicator.set_pos((self.coding_area_pos[0] - mini, self.coding_area_pos[1]))

    def update(self):
        if self.console.hidden:
            self.pos_indicator.set_real_pos((self.screen.get_width() - 85, self.screen.get_height() - 85))
        else:
            self.pos_indicator.set_real_pos((self.screen.get_width() - 435, self.screen.get_height() - 85))
        for obj in self.objects:
            obj.update()
        if not self.block_moving and pygame.mouse.get_pressed(3)[0] and\
          pygame.mouse.get_pos()[0] >= 400*(not self.objects[0].hidden):
            self.move_coding_area(pygame.mouse.get_rel())
        if self.objects[0].auto_link and len(self.objects) >= 4 and self.objects != self.objects_save:
            temp = [self.objects[-2].anchors[1], self.objects[-1].anchors[0]]
            temp2 = [self.objects[-1].anchors[1], self.objects[-2].anchors[0]]
            if not (tuple(temp) in self.links_list or tuple(temp2) in self.links_list) and\
              self.objects[-2].anchors[1].linked_anchor == None:
                try:
                    if self.objects[-2].anchors[1].code[::-1] != self.objects[-1].anchors[0].code:
                        create_link(self.objects[-2].anchors[1], self.objects[-1].anchors[0])
                        self.objects[-1].anchors[0].activated = False
                except:
                    pass
    
    def draw_buttons(self):
        pygame.draw.rect(self.screen, (10,10,10), self.read_code_rect,
                         border_bottom_left_radius=5)
        pygame.draw.polygon(self.screen, (119, 181, 63), ((self.read_code_rect.x+10, 8),
                                                          (self.read_code_rect.x+23, 17),
                                                          (self.read_code_rect.x+10, 26)))
        self.screen.blit(FONT.render("Lire le code", 0, (255, 255, 255)),
                         (self.read_code_rect.x+40, 5))
        pygame.draw.rect(self.screen, (10,10,10), self.validate_rect,
                         border_bottom_left_radius=5)
        pygame.draw.lines(self.screen, (119, 181, 63), False, (
                                (self.validate_rect.x+8, self.validate_rect.y+17),
                                (self.validate_rect.x+15, self.validate_rect.y+26),
                                (self.validate_rect.x+28, self.validate_rect.y+10)), 4)
        self.screen.blit(FONT.render("Valider", 0, (255, 255, 255)),
                         (self.validate_rect.x+43, self.validate_rect.y+5))
                            
    def log(self, text):
        self.console.log_console(text)

    def display(self):
        self.screen.fill((30,30,30))
        self.draw_buttons()
        temp2 = []
        for obj in self.objects[2:]:
            obj.draw()
            draw_links(self.links_list, self.screen)
            if obj.movable:
                temp2.append(obj)
            if obj.deleted:
                self.objects.remove(obj)
                for i in range(len(obj.anchors)):
                    temp = del_link(self.links_list, obj.anchors[i])
                    if temp != None:
                        if temp.out:
                            update_code(obj.anchors[i], temp)
                        else:
                            update_code(temp, obj.anchors[i])
                        temp.linked_anchor = None
        for obj in self.objects[:2]: # We place the console and
        # the menu at the end so that it is always in the foreground
            obj.draw()
        for obj in temp2:
            obj.draw()
        self.pos_indicator.draw()
        pygame.display.flip()
    
    def read_code(self):
        start = 0
        index = None
        for i in range(len(self.objects)):
            if isinstance(self.objects[i], StartBlock):
                start += 1
                index = i
        if start == 1:
            self.code = self.translator.lire_instructions(self.objects[index].whole_code,
                                                          self.console, self.character)
        elif start == 0:
            self.log("Il faut placer un bloc \"Début\"!")
        else:
            self.log("Vous avez placé plus d'un bloc \"Début\"!")
            return "Erreur"

    def run_code(self, code="default"):
        if code == "default":
            code = self.code
        self.translator.executer(code)

    def run(self):
        print(self.coding_area_pos)
        self.running = True
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(FPS)

def init_visual_coding(block_list, character=None):
    screen = pygame.display.set_mode((1280, 720))
    vc = VisualCoding(screen)
    vc.character = character
    menu = Menu(screen, vc)
    for value in block_list.values():
        for block in value:
            block.screen = menu.menu_area
            for anchor in block.anchors:
                if anchor != None:
                    anchor.screen = menu.menu_area
    menu.create_blocklist(block_list)
    console = Console(screen)
    vc.add_widgets(menu, console)
    vc.run()
    return vc.code, vc


if __name__ == '__main__':
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
        BlockWithInput("Afficher ", (20, (170,58,21)), (50, 0), temp, 9)]
    }
    init_visual_coding(block_list)
    pygame.quit()
