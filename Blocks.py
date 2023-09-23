import pygame
from math import pi

pygame.init()

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
ANCHOR_COLOR = pygame.Color("blue")
FONT = pygame.font.SysFont("Arial", 20)
FONT2 = pygame.font.SysFont("Arial", 10)
FPS = 60

#links_list = []

def blit_text(surface, text, pos, font, color=pygame.Color('white'),
              first_word=0, interlign_space=0, go_to_line=True):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space, word_height= font.size(' ')  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    x += first_word
    if words == []:
        return word_height + interlign_space, x
    for line in words[:-1]:
        for word in line:
            if word != "§":
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width and go_to_line:
                    x = pos[0]  # Reset the x.
                    y += word_height + interlign_space  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height + interlign_space  # Start on new row.
    for word in words[-1]:
        if word != "§":
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width and go_to_line:
                x = pos[0]  # Reset the x.
                y += word_height + interlign_space  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
    x -= space + 9
    return (y + word_height + interlign_space - pos[1], x + pos[0]) #  *2 to avoid
    # having the impression the text is compressed in the block

def create_link(anchor_out, anchor_in, links_list):
    links_list.append((anchor_out, anchor_in))
    anchor_in.activated, anchor_out.activated = True, False
    anchor_in.linked_anchor = anchor_out
    anchor_out.linked_anchor = anchor_in
    if anchor_out.rep_or_if:
        block = anchor_out.code[0]
        if isinstance(block, Repete):
            block.rep_code = anchor_in.code.copy()
            print(block.rep_code)
        elif isinstance(block,  IfElse):
            if anchor_out == block.anchors[2]:
                block.if_code = anchor_in.code.copy()
                print("if_code:", block.if_code)
            else:
                block.else_code = anchor_in.code.copy()
                print(block.else_code)
        for block in anchor_in.code:
            block.anchors[1].code += anchor_out.code
    else:
        for block in anchor_out.code:
            if len(block.anchors) == 2:
                try:
                    block.anchors[0].code += anchor_in.code
                except AttributeError:
                    block.whole_code += anchor_in.code
                    print("start_code:", block.whole_code)
            else:
                print("test", anchor_out.code[0], block.anchors[0].code)
                if anchor_out.code[0] in block.anchors[0].code:
                    block.anchors[0].code += anchor_in.code
                else:
                    if isinstance(block, Repete):
                        block.rep_code += anchor_in.code
                        print(block.rep_code)
                    elif isinstance(block,  IfElse):
                        if anchor_out.code[0] in block.if_code:
                            block.if_code += anchor_in.code
                            print("if_code:", block.if_code)
                        else:
                            block.else_code += anchor_in.code
                            print("else_code:", block.else_code)
        for block in anchor_in.code:
            block.anchors[1].code += anchor_out.code

def draw_links(links_list, screen):
    for link in links_list:
        x_distance = link[1].hit_box.x - link[0].hit_box.x
        y_distance = link[1].hit_box.y - link[0].hit_box.y
        if x_distance > 15 and y_distance > 15:
            for i in range(2):
                pygame.draw.arc(screen, (255,255,255), [link[i].hit_box.x - x_distance*0.5 + 8 - 2*i,
                                                        link[0].hit_box.y + 8,
                                                        abs(x_distance) + 4*i,
                                                        abs(y_distance)],
                                0 + pi*i, pi/2 + pi*i, 2)
        elif x_distance < -15 and y_distance > 15:
            for i in range(2):
                pygame.draw.arc(screen, (255,255,255), [link[0].hit_box.x + x_distance + 8,
                                                        link[i].hit_box.y - y_distance*0.5 + 8 - 2*i,
                                                        abs(x_distance),
                                                        abs(y_distance) + 4*i],
                                3*pi/2 + pi*i, 2*pi + pi*i, 2)
        elif x_distance > 15 and y_distance < -15:
            for i in range(2):
                pygame.draw.arc(screen, (255,255,255), [link[i].hit_box.x - x_distance*0.5 + 8 - 2*i,
                                                        link[0].hit_box.y + y_distance + 8,
                                                        abs(x_distance) + 4*i,
                                                        abs(y_distance) + abs(y_distance)*0.1*i],
                                3*pi/2 + pi*i, 2*pi + pi*i, 2)
        elif x_distance < -15 and y_distance < -15:
            for i in range(2):
                pygame.draw.arc(screen, (255,255,255), [link[0].hit_box.x + x_distance + 8,
                                                        link[i].hit_box.y + y_distance*0.5 + 8 - 2*i,
                                                        abs(x_distance) + abs(x_distance)*0.1*i,
                                                        abs(y_distance) + 4*i],
                                0 + pi*i, pi/2 + pi*i, 2)
        else:
            pygame.draw.line(screen, (255,255,255),
                            (link[0].hit_box.x + 7, link[0].hit_box.y + 8),
                            (link[1].hit_box.x + 7, link[1].hit_box.y + 8), 2)

def del_link(links_list, anchor_deleted):
    for link in links_list:
        for anchor in link:
            if anchor_deleted == anchor:
                links_list.remove(link)
                return anchor_deleted.linked_anchor

def update_code(_in, out):
    _in.linked_anchor = out.linked_anchor = None
    for block in out.code:
        if len(block.anchors) == 2:
            try:
                block.anchors[0].code = block.anchors[0].code[:- len(_in.code)]
            except AttributeError:
                block.whole_code = block.whole_code[:-len(_in.code)]
                print("start_code:", block.whole_code)
        elif out.code[0] in block.anchors[0].code:
            block.anchors[0].code = block.anchors[0].code[:-len(_in.code)]
        elif isinstance(block, Repete):
            block.rep_code = block.rep_code[:-len(_in.code)]
            print(block.rep_code)
        elif isinstance(block,  IfElse):
            if out.code[0] in block.if_code or out == block.anchors[2]:
                block.if_code = block.if_code[:-len(_in.code)]
                print(block.if_code)
            else:
                block.else_code = block.else_code[:-len(_in.code)]
                print(block.else_code)
    for block in _in.code:
        block.anchors[1].code = block.anchors[1].code[:-len(out.code)]

def handle_block_click(event, block, activated_anchor, links_list):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and\
      block.block.collidepoint(event.pos):
        if activated_anchor == None:
            block.anchors[1].update_link(links_list)
        else:
            if block.anchors[0] != None:
                block.anchors[0].update_link(links_list)

class InputBox:
    def __init__(self, x, y, w, h, screen, text='', max_chars=9999):
        self.screen = screen
        self.rect = pygame.Rect(x, y, w, h)
        self.initial_width = w
        self.color = COLOR_INACTIVE
        self.max_chars = max_chars
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.cursor_timer = 0
        self.autodel_time = FPS // 20
        self.clock = pygame.time.Clock()
        self.wait = 0

    def handle_event(self, event, screen_coord):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            rel_mouse_pos = tuple([event.pos[i] - screen_coord[i] for i in range(2)])
            if self.rect.collidepoint(rel_mouse_pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            if not self.active:
                self.cursor_timer = FPS // 2
                self.cursor_update()
            else:
                self.cursor_timer = 0
                
        if event.type == pygame.KEYDOWN:
            self.wait = 0
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = COLOR_INACTIVE
                    self.cursor_timer = FPS // 2
                    self.cursor_update()
                elif event.key == pygame.K_BACKSPACE:
                    # We erase the cursor and the function cursor_update
                    # will then erase the letter
                    self.text = self.text[:-1]
                    self.cursor_timer = 0
                    self.cursor_update()
                elif len(self.text) <= self.max_chars:
                    self.text = self.text[:-1] + event.unicode + " "
                    self.cursor_timer = 0
                    self.cursor_update()

    def cursor_update(self):
        if self.cursor_timer == 60:
            self.cursor_timer = 0
        if self.cursor_timer == 0:
            self.text = self.text[:-1] + "|"
            self.txt_surface = FONT.render(self.text, True, self.color)
        elif self.cursor_timer == FPS//2:
            self.text = self.text[:-1] + " "
            self.txt_surface = FONT.render(self.text, True, self.color)
        self.cursor_timer += 1
        self.wait += 1

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.initial_width, self.txt_surface.get_width()+5)
        if width != self.initial_width and self.text.endswith("|"):
            width += 1
        self.rect.w = width
        if self.active:
            keys = pygame.key.get_pressed()
            if self.wait >= FPS:
                if keys[pygame.K_BACKSPACE]:
                    if self.cursor_timer % self.autodel_time == 0:
                        self.text = self.text[:-1]
                        self.cursor_timer = 0
            self.cursor_update()
                    
    def draw(self):
        # Blit the text.
        self.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y))
        # Blit the rect.
        pygame.draw.rect(self.screen, self.color, self.rect, 2)

class ScrollBar:
    def __init__(self, screen, pos, size, display_width, max_width, vertical=True, initial_pos=0):
        self.screen = screen
        self.outer_rect = pygame.Rect(pos, size)
        if display_width > max_width:
            max_width = display_width
        if vertical:
            self.inner_rect = pygame.Rect((pos[0] + 1, pos[1] + size[1]*(initial_pos/max_width)),
                                          (size[0] - 2, size[1]*(display_width/max_width)))
        else:
            self.inner_rect = pygame.Rect((pos[0] + size[0]*(initial_pos/max_width), pos[1] + 1),
                                          (size[0]*(display_width/max_width), size[1] - 2))
        self.display_width = display_width
        self.movable = False
        self.max_width = max_width
        self.vertical = vertical
        self.max_value = self.max_width - self.display_width
        self.value = initial_pos

    def set_value(self, value):
        self.value = value
        if self.value > self.max_value:
            self.value = self.max_value + 1 # to avoid being 1 pixel short a the bottom
            # if the round number is truncated
        elif self.value < 0:
            self.value = 0
        self.update_pos()

    def update_pos(self):
        if self.vertical:
            self.inner_rect.y = self.outer_rect.y + self.outer_rect.h*(self.value/self.max_width)
        else:
            self.inner_rect.x = self.outer_rect.x + self.outer_rect.w*(self.value/self.max_width)

    def update(self):
        if pygame.mouse.get_pressed(3)[0] and self.movable:
            mouse_velo = pygame.mouse.get_rel()
            if self.vertical:
                if self.outer_rect.y <= self.inner_rect.y + mouse_velo[1] <=\
                  self.outer_rect.y + self.outer_rect.h*(1 - self.display_width/self.max_width):
                    self.inner_rect.y += mouse_velo[1]
                    self.value = self.max_width * ((self.inner_rect.y - self.outer_rect.y) /
                                                   self.outer_rect.h)
            else:
                if self.outer_rect.x <= self.inner_rect.x + mouse_velo[0] <=\
                  self.outer_rect.x + self.outer_rect.w*(1 - self.display_width/self.max_width):
                    self.inner_rect.x += mouse_velo[0]
                    self.value = self.max_width * ((self.inner_rect.x - self.outer_rect.x) /
                                                   self.outer_rect.w)
        return self.value
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN\
            and self.inner_rect.collidepoint(event.pos):
            pygame.mouse.get_rel()
            self.movable = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.movable = False

    def draw(self):
        pygame.draw.rect(self.screen, (100,100,100), self.outer_rect, border_radius=100)
        pygame.draw.rect(self.screen, (50,50,50), self.inner_rect, border_radius=100)

class ScrollRect:
    def __init__(self, screen, pos, size, display_size, total_size, initial_pos=(0,0)):
        self.screen = screen
        self.outer_rect = pygame.Rect(pos, size)
        self.inner_rect = pygame.Rect((pos[0] + size[0]*(initial_pos[0]/total_size[0]),
                                       pos[1] + size[1]*(initial_pos[1]/total_size[1])),
                                      (size[0]*(display_size[0]/total_size[0]),
                                       size[1]*(display_size[1]/total_size[1])))
        self.display_size = display_size
        self.movable = False
        self.total_size = total_size
        self.max_pos = [total_size[i] - display_size[i] for i in range(2)]
        self.pos = list(initial_pos)

    def set_pos(self, pos):
        self.pos = list(pos).copy()
        for i in range(2):
            if self.pos[i] > self.max_pos[i]:
                self.pos[i] = self.max_pos[i]
            elif self.pos[i] < 0:
                self.pos[i] = 0
        self.update_pos()
    
    def set_real_pos(self, pos):
        self.outer_rect.x = pos[0]
        self.outer_rect.y = pos[1]
        self.update_pos()

    def update_pos(self):
        self.inner_rect.y = self.outer_rect.y + self.outer_rect.h*(self.pos[1]/self.total_size[1])
        self.inner_rect.x = self.outer_rect.x + self.outer_rect.w*(self.pos[0]/self.total_size[0])

    def draw(self):
        pygame.draw.rect(self.screen, (100,100,100, 128), self.outer_rect)
        pygame.draw.rect(self.screen, (50,50,50, 128), self.inner_rect)

class link_anchor:
    def __init__(self, x, y, screen, color = ANCHOR_COLOR):
        self.screen = screen
        self.hit_box = pygame.Rect(x, y, 15, 15)
        self.color = color
        self.out = False
        self.rep_or_if = False
        self.code = []
        self.linked_anchor = None
        self.activated = False
    
    def handle_click(self, links_list, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the hit_box rect.
            if self.hit_box.collidepoint(event.pos):
                self.update_link(links_list)
    
    def update_link(self, links_list):
        if self.window.activated_anchor != None and not self.out:
            if self.window.activated_anchor.code[0] not in self.code:
                if self.linked_anchor != None:
                    del_link(links_list, self)
                    update_code(self, self.linked_anchor)
                create_link(self.window.activated_anchor, self, links_list)
                self.window.activated_anchor = None
        if self.out and ((not self.activated) or (self.activated and self.window.activated_anchor != self)):
            if self.linked_anchor != None:
                del_link(links_list, self)
                update_code(self.linked_anchor, self)
            self.activated = True
            self.window.activated_anchor = self
        else:
            self.activated = False
            self.window.activated_anchor = None

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.hit_box.x + 7, self.hit_box.y + 7), 7)
    
    def move(self, velo):
        self.hit_box.x += velo[0]
        self.hit_box.y += velo[1]

class BasicBlock:
    def __init__(self, inst, typo, pos, screen, w=250, min_h=50, rel_pos="default"):
        self.rel_pos_anchor = rel_pos
        self.inst = inst
        self.screen = screen
        self.font_size = typo[0]
        self.color = typo[1]
        self.in_menu = False
        self.menu = None
        self.deleted = False
        self.movable = False
        self.initial_width = w
        self.font = pygame.font.SysFont("Arial", self.font_size)
        self.text_height = blit_text(pygame.Surface((w-50, min_h)), self.inst, (10, 0),
                                     self.font)[0]
        self.text_box = pygame.Surface((w-50, max(min_h, self.text_height+25)-6))
        self.text_box.fill((30,30,30))
        self.block = pygame.Rect(pos[0], pos[1], w, max(min_h, self.text_height+25))
        self.create_anchor()

    def set_menu(self, menu):
        self.menu = menu
        self.menu_rect = self.menu.menu_area.get_rect()
    
    def set_screen(self, real_screen):
        self.real_screen = real_screen
        
    def create_anchor(self):
        if self.rel_pos_anchor == "default":
            self.rel_pos_anchor = (["7", "self.block.h/2 - 7"], ["self.block.w - 21", "self.block.h/2 - 7"])
        self.anchors = [link_anchor(self.block.x + eval(self.rel_pos_anchor[i][0]),
                                    self.block.y + eval(self.rel_pos_anchor[i][1]),
                                    self.screen)
                        for i in range(len(self.rel_pos_anchor))]
        for anchor in self.anchors:
            anchor.code.append(self)
        self.anchors[0].out, self.anchors[1].out = False, True
        self.anchors_text = [(FONT2.render(("in", "out")[i], True, ANCHOR_COLOR),
                              [self.block.x + eval(self.rel_pos_anchor[i][0]),
                               self.block.y + eval(self.rel_pos_anchor[i][1]) - 15]) for i in range(2)]
        # little adjustment for the x placement of "in"
        self.anchors_text[0][1][0] += 3
    
    def update_anchor_menu(self):
        for i in range(len(self.anchors)):
            self.anchors[i].hit_box.x = self.block.x + eval(self.rel_pos_anchor[i][0])
            self.anchors[i].hit_box.y = self.block.y + eval(self.rel_pos_anchor[i][1])
        
        for i in range(len(self.anchors_text)):
            self.anchors_text[i][1][0] = self.block.x + eval(self.rel_pos_anchor[i][0])
            self.anchors_text[i][1][1] = self.block.y + eval(self.rel_pos_anchor[i][1]) - 15
        
        self.anchors_text[0][1][0] += 3

    def draw_anchor(self):
        for anchor in self.anchors:
            if anchor != None:
                anchor.draw()
        for text in self.anchors_text:
            self.screen.blit(text[0], text[1])
    
    def update_anchor(self, velo):
        for anchor in self.anchors:
            if anchor != None:
                anchor.move(velo)
        for text in self.anchors_text:
            text[1][0] += velo[0]
            text[1][1] += velo[1]
    
    def handle_menu(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN\
            and self.block.collidepoint(event.pos) and event.button == 1:
            self.window.objects.append(BasicBlock(self.inst, (self.font_size, self.color),
                                      (self.block.x, self.block.y), self.real_screen))
            self.window.objects[-1].set_menu(self.menu)
            self.window.objects[-1].set_screen(self.real_screen)
            self.window.objects[-1].window = self.window
            for anchor in self.window.objects[-1].anchors:
                anchor.window = self.window
    
    def handle_anchor(self, event):
        for anchor in self.anchors:
            if anchor != None:
                anchor.handle_click(self.window.links_list, event)
    
    def draw(self):
        pygame.draw.rect(self.screen, (30,30,30), self.block, 0, 10)
        pygame.draw.rect(self.screen, self.color, self.block, 2, 10)
        blit_text(self.text_box, self.inst, (10, 10),
                  self.font, self.color)
        self.screen.blit(self.text_box, (self.block.x+25, self.block.y+3))
        self.draw_anchor()

    def handle_event(self, event):
        if not self.in_menu:
            self.handle_dragging(event)
            handle_block_click(event, self, self.window.activated_anchor, self.window.links_list)
            if self.menu.hidden or not self.menu_rect.collidepoint(pygame.mouse.get_pos()):
                self.handle_anchor(event)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_menu(event)

    def update(self):
        if not self.in_menu:
            if pygame.mouse.get_pressed(3)[0] and self.movable:
                mouse_velo = pygame.mouse.get_rel()
                self.update_pos(mouse_velo)
        else:
            self.update_anchor_menu()
    
    def handle_dragging(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN\
          and self.block.collidepoint(event.pos):
            pygame.mouse.get_rel()
            self.movable = True
            self.window.block_moving = True
        if event.type == pygame.MOUSEBUTTONUP:
            if self.block.colliderect(self.menu_rect) and not self.menu.hidden and\
              self.movable:
                self.deleted = True
            self.movable = False
            self.window.block_moving = False

    def update_pos(self, mouse_velo):
        cap = self.window.coding_area_pos
        mini = -400*(not self.menu.hidden)
        if not ((self.block.x + cap[0] + mouse_velo[0] < mini) or\
          (self.block.y + cap[1] + mouse_velo[1] < 0) or\
          (self.block.x + self.block.w + cap[0]  + mouse_velo[0] > self.screen.get_width()*3) or\
          (self.block.y + self.block.h + cap[1]  + mouse_velo[1] > self.screen.get_height()*3)):
            self.block.x += mouse_velo[0]
            self.block.y += mouse_velo[1]
            self.update_anchor(mouse_velo)

class StartBlock(BasicBlock):
    def __init__(self, typo, pos, screen, w=120, h=85):
        self.screen = screen
        self.font_size = typo[0]
        self.color = typo[1]
        self.in_menu = False
        self.menu = None
        self.deleted = False
        self.movable = False
        self.font = pygame.font.SysFont("Arial", self.font_size)
        self.text_box = pygame.Surface((w-10, h - 26))
        self.text_box.fill(self.color)
        self.block = pygame.Rect(pos[0], pos[1], w, h)
        self.whole_code = []
        self.create_anchor()

    def create_anchor(self):
        self.anchors = [None, link_anchor(self.block.x + self.block.w/2 - 7,
                                    self.block.y + self.block.h - 20,
                                    self.screen)]
        self.anchors[1].code.append(self)
        self.anchors[1].out = True
        self.anchors_text = [(FONT2.render(("out"), True, ANCHOR_COLOR),
                              [self.block.x + self.block.w/2 - 25,
                               self.block.y + self.block.h - 20])]
    
    def update_anchor_menu(self):
        self.anchors[1].hit_box.x = self.block.x + self.block.w/2 - 7
        self.anchors[1].hit_box.y = self.block.y + self.block.h - 20
        
        self.anchors_text[0][1][0] = self.block.x + self.block.w/2 - 25
        self.anchors_text[0][1][1] = self.block.y + self.block.h - 20
    
    def handle_menu(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN\
            and self.block.collidepoint(event.pos) and event.button == 1:
            self.window.objects.append(StartBlock((self.font_size, self.color),
                                      (self.block.x, self.block.y), self.real_screen))
            self.window.objects[-1].set_menu(self.menu)
            self.window.objects[-1].set_screen(self.real_screen)
            self.window.objects[-1].window = self.window
            for anchor in self.window.objects[-1].anchors[1:]:
                anchor.window = self.window
    
    def draw(self):
        pygame.draw.ellipse(self.screen, self.color,
                        pygame.Rect((self.block.x, self.block.y),
                                    (self.block.w, 60)))
        pygame.draw.rect(self.screen, self.color,
                         pygame.Rect((self.block.x, self.block.y + 30),
                                     (self.block.w, self.block.h - 30)),
                         0, border_bottom_left_radius = 7,
                         border_bottom_right_radius = 7)
        blit_text(self.text_box, "Début", (20, 0),
                  self.font, (255,255,255))
        self.screen.blit(self.text_box, (self.block.x+5, self.block.y+23))
        self.draw_anchor()
        
class BlockWithInput(BasicBlock):
    def __init__(self, inst, typo, pos, screen, input_index, w=250, min_h=50, max_chars=9999, rel_pos="default",
                 interlign_space=0):
        self.rel_pos_anchor = rel_pos
        self.inst = inst
        self.screen = screen
        self.font_size = typo[0]
        self.color = typo[1]
        self.in_menu = False
        self.menu = None
        self.deleted = False
        self.input_index = input_index
        self.max_chars = max_chars
        self.movable = False
        self.initial_width = w
        self.font = pygame.font.SysFont("Arial", self.font_size)
        self.inter_space = interlign_space
        self.word_height = self.font.size(" ")[1] + interlign_space
        self.text_height = blit_text(pygame.Surface((w-50, min_h)), self.inst, (10, 0),
                                     self.font, interlign_space=self.inter_space)[0]
        self.text_box = pygame.Surface((w-50, max(min_h, self.text_height+25)-6))
        self.block = pygame.Rect(pos[0], pos[1], w, max(min_h, self.text_height+25))
        self.create_anchor()
        self.create_input()
    
    def create_input(self):
        y, x = blit_text(self.text_box, self.inst[:self.input_index], (10, 0),
                            self.font, interlign_space=self.inter_space)
        y -= self.word_height
        self.input = InputBox(x, y+10, 15, 23,
                              self.text_box, max_chars=self.max_chars)
        self.text_box.fill((30,30,30))
        
    def handle_event(self, event):
        if not self.in_menu:
            self.handle_dragging(event)
            handle_block_click(event, self, self.window.activated_anchor, self.window.links_list)
            if self.menu.hidden or not self.menu_rect.collidepoint(pygame.mouse.get_pos()):
                self.handle_anchor(event)
                self.input.handle_event(event, (self.block.x+25, self.block.y))
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_menu(event)
    
    def handle_menu(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN\
            and self.block.collidepoint(event.pos) and event.button == 1:
            self.window.objects.append(BlockWithInput(self.inst, (self.font_size, self.color),
                                      (self.block.x, self.block.y), self.real_screen, self.input_index,
                                      max_chars=self.max_chars, w=self.initial_width))
            self.window.objects[-1].set_menu(self.menu)
            self.window.objects[-1].set_screen(self.real_screen)
            self.window.objects[-1].window = self.window
            for anchor in self.window.objects[-1].anchors:
                anchor.window = self.window
    
    def update(self):
        if not self.in_menu:
            if pygame.mouse.get_pressed(3)[0] and self.movable:
                mouse_velo = pygame.mouse.get_rel()
                self.update_pos(mouse_velo)
            self.input.update()
            self.block.w = max(self.initial_width,
                                self.input.rect.x + self.input.rect.w + 50)
            if self.block.w != self.text_box.get_width() + 50:
                self.text_box = pygame.Surface((self.block.w - 50,
                                                self.text_box.get_height()))
                self.input.screen = self.text_box
                self.update_anchor_menu()
        else:
            self.update_anchor_menu()
        
    
    def draw(self):
        pygame.draw.rect(self.screen, (30,30,30), self.block, 0, 10)
        pygame.draw.rect(self.screen, self.color, self.block, 2, 10)
        self.draw_anchor()
        self.text_box.fill((30,30,30))
        a = blit_text(self.text_box, self.inst[:self.input_index], (10, 10),
                  self.font, self.color, interlign_space=self.inter_space)[0]
        self.input.draw()
        b = blit_text(self.text_box, self.inst[self.input_index:], (10, self.input.rect.y),
                  self.font, self.color, first_word=self.input.rect.x + self.input.rect.w - 10,
                  interlign_space=self.inter_space)[0]
        if a + b - self.word_height != self.text_height:
            diff = a + b - self.word_height - self.text_height
            self.block.h += diff
            self.text_box = pygame.Surface((self.text_box.get_width(),
                                self.text_box.get_height() + diff))
            self.text_height += diff
            self.input.screen = self.text_box
            self.update_anchor_menu()
        self.screen.blit(self.text_box, (self.block.x+25, self.block.y+3))

class BlockWithInputs(BlockWithInput):
    def create_input(self):
        if self.max_chars == 9999:
            self.max_chars = [9999 for i in range(len(self.input_index))]
        start, x, y = 0, 10, 0
        self.max_width = [0,0,0]
        self.inputs = []
        for index in self.input_index:
            y_bis, x = blit_text(self.text_box, self.inst[start:index], (10, y),
                             self.font, first_word=x-10, interlign_space=self.inter_space)
            y += y_bis - self.word_height
            if x + 15 < self.text_box.get_width(): # if the input_box is to long for the block
                 # so that the inputs are not too far from the text
                self.inputs.append(InputBox(x, y+10, 15, 23,
                                    self.text_box, max_chars=self.max_chars[self.input_index.index(index)]))
            else:
                y += self.word_height
                x = 10
                self.inputs.append(InputBox(10, y+10, 15, 23,
                                    self.text_box, max_chars=self.max_chars))
            x += self.inputs[-1].rect.w
            start = index
        y += blit_text(self.text_box, self.inst[start:], (10, y),
                        self.font, first_word=x-10, interlign_space=self.inter_space)[0]
        diff = y - self.text_height
        self.block.h += diff
        self.text_box = pygame.Surface((self.text_box.get_width(),
                            self.text_box.get_height() + diff))
        self.text_height = y
        for input_ in self.inputs:
                input_.screen = self.text_box
        self.text_box.fill((30,30,30))
    
    def handle_menu(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN\
            and self.block.collidepoint(event.pos) and event.button == 1:
            self.window.objects.append(BlockWithInputs(self.inst, (self.font_size, self.color),
                                      (self.block.x, self.block.y), self.real_screen, self.input_index,
                                      max_chars=self.max_chars, interlign_space=self.inter_space))
            self.window.objects[-1].set_menu(self.menu)
            self.window.objects[-1].set_screen(self.real_screen)
            self.window.objects[-1].window = self.window
            for anchor in self.window.objects[-1].anchors:
                anchor.window = self.window
    
    def handle_event(self, event):
        if not self.in_menu:
            self.handle_dragging(event)
            handle_block_click(event, self, self.window.activated_anchor, self.window.links_list)
            if self.menu.hidden or not self.menu_rect.collidepoint(pygame.mouse.get_pos()):
                self.handle_anchor(event)
                for input_ in self.inputs:
                    input_.handle_event(event, (self.block.x+25, self.block.y))
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_menu(event)

    def draw_and_update_inputs_pos(self):
        start, x, y = 0, 10, 10
        for i in range(len(self.input_index)):
            if self.inputs[i].rect.y == y:
                go_to_line = False
            else:
                go_to_line = True
            y_bis, x = blit_text(self.text_box, self.inst[start:self.input_index[i]], (10, y),
                             self.font, self.color, x-10, interlign_space=self.inter_space,
                             go_to_line=go_to_line)
            y += y_bis - self.word_height
            if y >= self.inputs[i].rect.y:
                self.inputs[i].rect.x = x
            else:
                self.inputs[i].rect.x = 10
                x = 10
                y = self.inputs[i].rect.y
            x += self.inputs[i].rect.w
            self.inputs[i].draw()
            start = self.input_index[i]
        y += blit_text(self.text_box, self.inst[start:], (10, y), self.font,
                       self.color, x-10, interlign_space=self.inter_space)[0]
        cumulated_height = y - 10  # because we begin with a height of 10
        if cumulated_height != self.text_height:
            diff = cumulated_height - self.text_height
            self.block.h += diff
            self.text_box = pygame.Surface((self.text_box.get_width(),
                                self.text_box.get_height() + diff))
            self.text_height = cumulated_height
            for input_ in self.inputs:
                input_.screen = self.text_box
            self.update_anchor_menu()
    
    def update(self):
        if not self.in_menu:
            self.update_anchor_menu()
            if pygame.mouse.get_pressed(3)[0] and self.movable:
                mouse_velo = pygame.mouse.get_rel()
                self.update_pos(mouse_velo)
            max_width = 0
            for input_ in self.inputs:
                input_.update()
                input_width = input_.rect.x + input_.rect.w + 50
                if input_width > max_width:
                    max_width = input_width
            if self.max_width[0] != max_width:
                if self.max_width[1] == max_width:
                    self.max_width[0], self.max_width[1] = self.max_width[1], self.max_width[0]
                    self.max_width[2] += 1
                else:
                    self.max_width[1] = self.max_width[0]
                    self.max_width[0] = max_width
                    self.max_width[2] = 0
            if self.max_width[2] >= 1:
                max_width = max(self.max_width[0], self.max_width[1])
            self.block.w = max(self.initial_width, max_width)
            if self.block.w != self.text_box.get_width() + 50:
                self.text_box = pygame.Surface((self.block.w - 50,
                                                self.text_box.get_height()))
                for input_ in self.inputs:
                    input_.screen = self.text_box
                self.update_anchor_menu()
        else:
            self.update_anchor_menu()

    def draw(self):
        pygame.draw.rect(self.screen, (30,30,30), self.block, 0, 10)
        pygame.draw.rect(self.screen, self.color, self.block, 2, 10)
        self.draw_anchor()
        self.text_box.fill((30,30,30))
        self.draw_and_update_inputs_pos()
        self.screen.blit(self.text_box, (self.block.x+25, self.block.y+3))

class Repete(BlockWithInput):
    def __init__(self, inst, typo, pos, screen, input_index=None, w=250, min_h=50, max_chars=9999, rel_pos="default",
                 interlign_space=0):
        BlockWithInput.__init__(self, inst, typo, pos, screen, input_index, w=w,
                                min_h=min_h, max_chars=max_chars, rel_pos=rel_pos,
                                interlign_space=interlign_space)
        self.block = pygame.Rect(pos[0], pos[1], w, max(min_h, self.text_height+45))
        self.rel_pos_anchor = rel_pos
        self.rep_code = []
        self.create_anchor()
        
    
    def create_anchor(self):
        if self.rel_pos_anchor == "default":
            self.rel_pos_anchor = (["7", "self.block.h/2 - 7"], ["self.block.w - 21", "self.block.h/2 - 7"],
                                   ["self.block.w/2 - 7", "self.block.h - 20"])
        self.anchors = [link_anchor(self.block.x + eval(self.rel_pos_anchor[i][0]),
                                    self.block.y + eval(self.rel_pos_anchor[i][1]),
                                    self.screen)
                        for i in range(3)]
        for anchor in self.anchors:
            anchor.code.append(self)
        self.anchors[0].out, self.anchors[1].out, self.anchors[2].out = False, True, True
        self.anchors[0].rep_or_if, self.anchors[1].rep_or_if, self.anchors[2].rep_or_if = False, False, True
        self.anchors_text = [(FONT2.render(("in", "out", "rep")[i], True, ANCHOR_COLOR),
                              [self.block.x + eval(self.rel_pos_anchor[i][0]),
                               self.block.y + eval(self.rel_pos_anchor[i][1]) - 15]) for i in range(3)]
        # adjustements for the placement of "rep"
        self.anchors_text[2][1][0] -= 15
        self.anchors_text[2][1][1] += 15
        # little adjustment for the x placement of "in"
        self.anchors_text[0][1][0] += 3
    
    def handle_menu(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN\
            and self.block.collidepoint(event.pos) and event.button == 1:
            self.window.objects.append(Repete(self.inst, (self.font_size, self.color),
                                      (self.block.x, self.block.y), self.real_screen, self.input_index,
                                      max_chars=self.max_chars, w=self.initial_width))
            self.window.objects[-1].set_menu(self.menu)
            self.window.objects[-1].set_screen(self.real_screen)
            self.window.objects[-1].window = self.window
            for anchor in self.window.objects[-1].anchors:
                anchor.window = self.window
    
    def update_anchor_menu(self):
        for i in range(len(self.anchors)):
            self.anchors[i].hit_box.x = self.block.x + eval(self.rel_pos_anchor[i][0])
            self.anchors[i].hit_box.y = self.block.y + eval(self.rel_pos_anchor[i][1])
        
        for i in range(len(self.anchors_text)-1):
            self.anchors_text[i][1][0] = self.block.x + eval(self.rel_pos_anchor[i][0])
            self.anchors_text[i][1][1] = self.block.y + eval(self.rel_pos_anchor[i][1]) - 15

        self.anchors_text[2][1][0] = self.block.x + eval(self.rel_pos_anchor[2][0]) - 15
        self.anchors_text[2][1][1] = self.block.y + eval(self.rel_pos_anchor[2][1])
        
        self.anchors_text[0][1][0] += 3

class While(Repete):
    def __init__(self, inst, typo, pos, screen, w=250, min_h=50, rel_pos="default"):
        BasicBlock.__init__(self, inst, typo, pos, screen, w=w, min_h=min_h, rel_pos=rel_pos)
        self.block = pygame.Rect(pos[0], pos[1], w, max(min_h, self.text_height+45))
        self.rel_pos_anchor = rel_pos
        self.rep_code = []
        self.create_anchor()
    
    def update(self):
        BasicBlock.update(self)
    
    def handle_event(self, event):
        BasicBlock.handle_event(self, event)
    
    def draw(self):
        BasicBlock.draw(self)
    
    def handle_menu(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN\
            and self.block.collidepoint(event.pos) and event.button == 1:
            self.window.objects.append(While(self.inst, (self.font_size, self.color),
                                 (self.block.x, self.block.y), self.real_screen,
                                 w=self.initial_width))
            self.window.objects[-1].set_menu(self.menu)
            self.window.objects[-1].set_screen(self.real_screen)
            self.window.objects[-1].window = self.window
            for anchor in self.window.objects[-1].anchors:
                anchor.window = self.window
    
class IfElse(BasicBlock):
    def __init__(self, inst, typo, pos, screen, Else=False,  w=250, min_h=50, start=0):
        self.Else = Else
        self.start_pos = start
        self.if_code = []
        self.else_code = []
        BasicBlock.__init__(self, inst, typo, pos, screen, w=w, min_h=min_h)
    
    def create_anchor(self):
        self.rel_pos_anchor = [["7", "self.block.h/2 - 7"], ["self.block.w - 21", "self.block.h/2 - 7"],
                               ["self.block.w/2-7", "19"]]
        if self.Else:
            self.rel_pos_anchor.append(["self.block.w/2-7", "42"])
        BasicBlock.create_anchor(self)
        for anchor in self.anchors[2:]:
            anchor.out = True
            anchor.rep_or_if = True
    
    def handle_menu(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN\
            and self.block.collidepoint(event.pos) and event.button == 1:
            self.window.objects.append(IfElse(self.inst, (self.font_size, self.color),
                                   (self.block.x, self.block.y), self.real_screen,
                                   w=self.initial_width, Else=self.Else,
                                   start=self.start_pos))
            self.window.objects[-1].set_menu(self.menu)
            self.window.objects[-1].set_screen(self.real_screen)
            self.window.objects[-1].window = self.window
            for anchor in self.window.objects[-1].anchors:
                anchor.window = self.window
    
    def draw(self):
        pygame.draw.rect(self.screen, (30,30,30), self.block, 0, 10)
        pygame.draw.rect(self.screen, self.color, self.block, 2, 10)
        blit_text(self.text_box, self.inst, (10, 10),
                  self.font, self.color, first_word=self.start_pos)
        self.screen.blit(self.text_box, (self.block.x+25, self.block.y+3))
        self.draw_anchor()