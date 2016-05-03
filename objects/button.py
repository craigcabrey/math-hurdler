
import pygame

class Button(object):

    def __init__(self, text, font, font_color, height, width, color, border_color=None, border_thickness=None):
        self.image = pygame.Surface((height,width))
        self.rect = self.image.get_rect()
        if border_thickness and border_color:
            self.image.fill(border_color)
            self.image.fill(color,self.rect.inflate(border_thickness,border_thickness))
        else:
            self.image.fill(color)
        self.font = font
        self.font_color = font_color
        self.set_text(text)

    def draw(self, surface):
        self.label_rect.center = (self.rect.x+self.image.get_width()/2, self.rect.y+self.image.get_height()/2)
        surface.blit(self.image,self.rect)
        surface.blit(self.label,self.label_rect)

    def mouse_click(self, mouse, action):
        if self.rect.collidepoint(mouse):
            action()

    def set_text(self, text):
        self.text = text
        self.label = self.font.render(self.text,1,self.font_color)
        self.label_rect = self.label.get_rect()
