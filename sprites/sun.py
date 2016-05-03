
import pygame

class Sun(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        sun = pygame.image.load('./assets/images/sun.png').convert_alpha()
        self.image = pygame.transform.scale(sun, (sun.get_width() / 2, sun.get_height() / 2))
        self.rect = self.image.get_rect()
