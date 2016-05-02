#!/usr/bin/python
import pygame
import random
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
        self.direction = 1

        self.circle_size = 150

    def set_paused(self, paused):
        self.paused = paused

    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass

    # The main game loop.
    def run(self):
        self.running = True

        screen = pygame.display.get_surface()
        screen_size = screen.get_size()

        background = pygame.Surface(screen_size)
        background = background.convert()
        background.fill((126,192,238))

        ground = pygame.Surface( (screen_size[0], screen_size[1]/5) )
        ground = ground.convert()
        ground.fill((127,96,0))

        grass = pygame.draw.line(ground,(0,255,0),(0,0), (ground.get_width(),0), 15)

        horse = pygame.image.load('./assets/images/color_unicorn.png')
        horse = pygame.transform.scale(horse,(640/3,472/3))

        hurdle = pygame.image.load('./assets/images/hurdle.png')
        hurdle = pygame.transform.scale(hurdle,(hurdle.get_height()/3,hurdle.get_width()/3))

        display_info = pygame.display.Info();

        while self.running:
            # Pump GTK messages.
            while Gtk.events_pending():
                Gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.direction = 1

            # Move the ball
            if not self.paused:
                self.x += self.vx * self.direction
                if self.direction == 1 and self.x > screen.get_width() + 50:
                    self.x = -50
                elif self.direction == -1 and self.x < -50:
                    self.x = screen.get_width() + 50

                self.y += self.vy
                if self.y > screen.get_height() - 50:
                    self.y = screen.get_height() - 50
                    self.vy = -self.vy

                self.vy += 5

            # Clear Display
            screen.fill((255, 255, 255))  # 255 for white

            screen.blit(background, (0,0))
            screen.blit(ground, (0,screen_size[1]-ground.get_height()))
            screen.blit(horse,(100,(display_info.current_h - horse.get_height()-ground.get_height())))
            screen.blit(hurdle,(self.x,(display_info.current_h - hurdle.get_height()-ground.get_height())))

            # Flip Display
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
