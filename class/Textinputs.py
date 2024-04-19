import pygame

class Textlabel():
    def __init__(self, width, height, text, fontsize, colour):
        self.font = pygame.font.Font(None, fontsize)
        self.text = text
        self.colour = colour
        self.width = width
        self.height = height
        self.visible = False

    def draw(self, screen):
        if self.visible:
            textout = self.font.render(self.text, 1, self.colour)
            screen.blit(textout, (self.width, self.height))

class Textbox():
    def __init__(self, width, height, size_x, size_y, fontsize, predefined_text=""):
        self.font = pygame.font.Font(None, fontsize)
        self.user_text = predefined_text
        self.input_rect = pygame.Rect(width, height, size_x, size_y)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('chartreuse4')
        self.color = self.color_passive
        self.active = False
        self.visible = False

    def draw(self, screen):
        if self.visible == True:
            pos = pygame.mouse.get_pos()
            if self.input_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]:
                    self.active = True
            else:
                self.active = False

            if self.active:
                self.color = self.color_active
            else:
                self.color = self.color_passive

            pygame.draw.rect(screen, self.color, self.input_rect)
            text_surface = self.font.render(self.user_text, True, (255, 255, 255))
            screen.blit(text_surface, (self.input_rect.x+5, self.input_rect.y+5))
            self.input_rect.w = max(100, text_surface.get_width()+10)

    def add_text(self, text):
        if self.active:
            self.user_text += text
    def remove_char(self):
        if self.active:
            self.user_text = self.user_text[:-1]
