#!/usr/bin/python
import pygame
import random
import os
from gi.repository import Gtk


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

        grass = pygame.draw.line(ground,(0, 255, 0), (0, 0), (ground.get_width(), 0), ground.get_height()/2)

        sun = pygame.image.load(self.get_asset_path('sun.png'))
        sun = pygame.transform.scale(sun, (sun.get_width() / 2, sun.get_height() / 2))

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
            while Gtk.events_pending():
                Gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.direction = 1

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

            screen.blit(question_board, (screen_size[0] / 4, screen_size[1] / 5))
            question_board.blit(question_label, (10,10))
            question_board.blit(question, (10,question_label.get_height()+10))

            sun_x = screen_size[1] + sun.get_width()
            sun_y = 0
            screen.blit(sun, (sun_x,sun_y))
            screen.blit(score_label, (sun_x+sun.get_width()/4,sun_y+sun.get_height()/3))
            screen.blit(points_label, (sun_x+sun.get_width()/4, sun_y+sun.get_height()/3+score_label.get_height()))

            screen.blit(ground, (0, screen_size[1] - ground.get_height()))
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
