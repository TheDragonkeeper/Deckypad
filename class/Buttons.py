import pygame

class Button():
    def __init__(self, x, y, image, scale, onetime):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.onetime = onetime
        self.visible = True

    def draw(self, screen):
        if self.visible:
            do_something = False
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]:
                    if not self.clicked:
                        self.clicked = True
                        do_something = True
                        if self.onetime:
                            self.visible = False
            if not self.onetime:
                if not pygame.mouse.get_pressed()[0]:
                    self.clicked = False
            screen.blit(self.image, (self.rect.x, self.rect.y))
            return do_something
