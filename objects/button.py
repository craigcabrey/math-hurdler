
import pygame

class Button(object):
    def __init__(self, text, font, font_color, height, width, color, border_color=None, border_thickness=None):
        self.height = height
        self.width = width
        self.border_color = border_color
        self.border_thickness = border_thickness
        self.image = pygame.Surface((self.height,self.width))
        self.rect = self.image.get_rect()
        self.set_color(color)
        self.font = font
        self.font_color = font_color
        self.set_text(text)

    def draw(self, surface):
        self.label_rect.center = (self.rect.x+self.image.get_width()/2, self.rect.y+self.image.get_height()/2)
        surface.blit(self.image,self.rect)
        surface.blit(self.label,self.label_rect)

    def mouse_click(self, mouse, action, *args):
        if self.rect.collidepoint(mouse):
            action(*args)

    def set_text(self, text):
        self.text = text
        self.label = self.font.render(self.text,1,self.font_color)
        self.label_rect = self.label.get_rect()

    def set_color(self, color):
        self.color = color
        print(self.color)
        if self.border_thickness and self.border_color:
            self.image.fill(self.border_color)
            self.rect = self.image.get_rect()
            box = self.rect.inflate(self.border_thickness,self.border_thickness)
            self.image.fill(self.color,box)
        else:
            self.image.fill(self.color)
