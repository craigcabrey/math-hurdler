import pygame

class Horse(pygame.sprite.Sprite):

    BASE = 'base'
    JUMP = 'jump'
    GALLOP = 'gallop'
    DEAD = 'dead'

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        horse = pygame.image.load('./assets/images/color_unicorn.png').convert_alpha()
        self.horse_base = pygame.transform.scale(horse,(horse.get_width() / 3, horse.get_height() / 3))
        self.horse_jump = pygame.transform.rotate(self.horse_base,45)
        self.horse_gallop = pygame.transform.rotate(self.horse_base, -15)
        self.horse_dead = pygame.transform.rotate(self.horse_base,-150)
        self.active_horse = Horse.BASE
        self.image = self.horse_base
        self.rect = self.image.get_rect()
        

    def set_horse(self,horse):
        if (horse == Horse.BASE):
            self.image = self.horse_base
        elif (horse == Horse.JUMP):
            self.image = self.horse_jump
        elif (horse == Horse.GALLOP):
            self.image = self.horse_gallop
        elif (horse == Horse.DEAD):
            self.image = self.horse_dead
        self.active_horse = horse
