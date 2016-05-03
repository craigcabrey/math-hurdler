#!/usr/bin/env python2

import gi

gi.require_version('Gtk', '3.0')

import gi.repository.Gtk
import pygame
import random
import os
from sprites.sun import Sun
from objects.button import Button

class MathHurdler:
    def __init__(self):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()

        self.x = -100
        self.y = 100

        self.vx = 10
        self.vy = 0

        self.paused = False
        self.direction = -1

        self.circle_size = 150

        self.horse_change_semaphore = 3
        self.horse_change = 0;

        self.font = pygame.font.SysFont("monospace", 36)
        self.lg_font = pygame.font.SysFont("monospace", 72)

        self.hurdle_number = 1

        self.points = 0;

    def set_paused(self, paused):
        self.paused = paused

    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass

    def get_asset_path(self, asset_name):
        return os.path.join('./assets/images', asset_name)

    # The main game loop.
    def run(self):
        self.running = True

        display_info = pygame.display.Info();
        background_color = (126, 192, 238)

        screen = pygame.display.get_surface()
        screen_size = screen.get_size()

        ground = pygame.Surface((screen_size[0], screen_size[1] / 3))
        ground = ground.convert()
        ground.fill((127, 96, 0))

        button_panel = pygame.Surface((screen_size[0]/3, screen_size[1] / 7))

        button_a = Button('3/4', self.lg_font,(0,0,0), button_panel.get_width()/2,
                           button_panel.get_height()/2, (255,255,255), (0,0,0), -2)

        button_b = Button('0', self.lg_font,(0,0,0), button_panel.get_width()/2,
                           button_panel.get_height()/2, (255,255,255), (0,0,0), -2)

        button_c = Button('1', self.lg_font,(0,0,0), button_panel.get_width()/2,
                           button_panel.get_height()/2, (255,255,255), (0,0,0), -2)

        button_d = Button('1/4', self.lg_font,(0,0,0), button_panel.get_width()/2,
                           button_panel.get_height()/2, (255,255,255), (0,0,0), -2)

        grass = pygame.draw.line(ground,(0, 255, 0), (0, 0), (ground.get_width(), 0), ground.get_height()/2)

        score_label = self.lg_font.render(str(self.points),1,(0,0,0))
        points_label = self.lg_font.render('POINTS',1,(0,0,0))

        horse = pygame.image.load(self.get_asset_path('color_unicorn.png'))
        horse = pygame.transform.scale(horse,(horse.get_width() / 3, horse.get_height() / 3))
        horse_jump = pygame.transform.rotate(horse,45)
        horse_gallop = pygame.transform.rotate(horse, -15)

        active_horse = horse_gallop;

        horse_x = display_info.current_h/3;

        hurdle = pygame.image.load('./assets/images/hurdle.png')
        hurdle = pygame.transform.scale(hurdle,(hurdle.get_height()/3,hurdle.get_width()/3))

        hurdle_y = display_info.current_h - hurdle.get_height() - (2*ground.get_height()/3)

        question_board = pygame.Surface((screen_size[0]/3, screen_size[1] / 5))
        question_board = question_board.convert()
        question_board.fill((255, 255, 255))

        question_label = self.font.render("Hurdle #" + str(self.hurdle_number), 1, (0,0,0))
        question = self.lg_font.render("3/4 + 1/4 = ?", 1, (0,0,0))

        while self.running:
            while gi.repository.Gtk.events_pending():
                gi.repository.Gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.direction = 1
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused

            screen_size = screen.get_size()

            if not self.paused:

                self.x += self.vx * self.direction
                if self.direction == 1 and self.x > screen.get_width() + 50:
                    self.x = -50
                elif self.direction == -1 and self.x < -50:
                    self.x = screen.get_width() + 50
                self.y = display_info.current_h - horse.get_height() - ground.get_height();

                hurdle_rect = hurdle.get_rect(topleft=(self.x,hurdle_y))
                horse_rect = horse.get_rect(topleft=(horse_x,self.y))

                if ( (active_horse == horse_jump) and (not hurdle_rect.colliderect(horse_rect)) ):
                    active_horse = horse
                    self.hurdle_number += 1
                    question_board.fill((255, 255, 255))
                    question_label = self.font.render("Hurdle #" + str(self.hurdle_number), 1, (0,0,0))
                    self.points += 100
                    score_label = []
                    score_label = self.lg_font.render(str(self.points),1,(0,0,0))

                if (self.horse_change == self.horse_change_semaphore):
                    if (active_horse == horse):
                        active_horse = horse_gallop
                    elif (active_horse == horse_gallop):
                        active_horse = horse
                    self.horse_change = 0

                self.horse_change += 1

                # Check if hurdle and horse in same spot.
                if hurdle_rect.colliderect(horse_rect):
                    active_horse = horse_jump
                    self.y -= 200

            # Set the "sky" color to blue
            screen.fill(background_color)

            sun = Sun()
            sun.rect.x = screen_size[1] + sun.image.get_width()
            sun.rect.y = 0

            allsprites = pygame.sprite.RenderPlain((sun))
            allsprites.draw(screen)

            screen.blit(question_board, (screen_size[0] / 4, screen_size[1] / 5))
            question_board.blit(question_label, (10,10))
            question_board.blit(question, (10,question_label.get_height()+10))

            screen.blit(score_label, (sun.rect.x+sun.image.get_width()/4,sun.rect.y+sun.image.get_height()/3))
            screen.blit(points_label, (sun.rect.x+sun.image.get_width()/4, sun.rect.y+sun.image.get_height()/3+score_label.get_height()))

            screen.blit(ground, (0, screen_size[1] - ground.get_height()))
            button_panel_x = ground.get_width()/4
            button_panel_y = screen_size[1] - ground.get_height() + ground.get_height()/3+10
            screen.blit(button_panel, (button_panel_x,button_panel_y))

            button_a.rect.x = button_panel_x
            button_a.rect.y = button_panel_y
            button_a.draw(screen)

            button_b.rect.x = button_panel_x + button_a.image.get_width()
            button_b.rect.y = button_panel_y
            button_b.draw(screen)

            button_c.rect.x = button_panel_x
            button_c.rect.y = button_panel_y + button_a.image.get_height()
            button_c.draw(screen)

            button_d.rect.x = button_panel_x + button_c.image.get_width()
            button_d.rect.y = button_panel_y + button_b.image.get_height()
            button_d.draw(screen)

            screen.blit(active_horse, (horse_x, self.y))
            screen.blit(hurdle,(self.x,hurdle_y))

            # Draw the frame
            pygame.display.flip()

            # Try to stay at 30 FPS
            self.clock.tick(30)



# This function is called when the game is run directly from the command line:
# ./TestGame.py
def main():
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    game = MathHurdler()
    game.run()

if __name__ == '__main__':
    main()
