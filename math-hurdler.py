#!/usr/bin/env python2

import pygame
import random
import os

from sprites.sun import Sun
from objects.button import Button
from question import Question

class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    SKYBLUE = (126, 192, 238)
    BROWN = (127, 96, 0)
    GREEN = (0, 255, 0)

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
        self.horse_change = 0

        self.font = pygame.font.SysFont('monospace', 36)
        self.lg_font = pygame.font.SysFont('monospace', 60)

        self.hurdle_number = 0

        self.points = 0

        self.question = Question()

        self.question_text_label = self.lg_font.render(
            str(self.question),
            1,
            Color.BLACK
        )

        self.question_label = self.font.render(
            'Hurdle #' + str(self.hurdle_number),
            1,
            Color.BLACK
        )

        self.score_label = self.lg_font.render(
            str(self.points),
            1,
            Color.BLACK
        )

        self.buttons = []

    def set_paused(self, paused):
        self.paused = paused

    def set_gameover(self, gameover):
        self.gameover = gameover

    def set_playing(self, playing):
        self.playing = playing
        self.set_paused(False)
        self.set_gameover(False)

    def get_asset_path(self, asset_name):
        return os.path.join('./assets/images', asset_name)

    # The main game loop.
    def run(self):
        self.running = True
        self.playing = False
        self.gameover = False
        self.paused = False
        last_answer = -1
        question_dirty = True

        self.score = 0

        display_info = pygame.display.Info()
        background_color = Color.SKYBLUE

        screen = pygame.display.get_surface()
        screen_size = screen.get_size()

        ground = pygame.Surface((screen_size[0], screen_size[1] / 3))
        ground = ground.convert()
        ground.fill(Color.BROWN)

        button_panel = pygame.Surface((screen_size[0]/3, screen_size[1] / 7))

        self.buttons = [
            Button(
                str(self.question.answers[i]),
                self.lg_font,
                Color.BLACK,
                button_panel.get_width() / 2,
                button_panel.get_height() / 2,
                Color.WHITE,
                Color.BLACK,
                -2
            ) for i in range(4)
        ]

        grass = pygame.draw.line(
            ground,
            Color.GREEN,
            (0, 0),
            (ground.get_width(), 0),
            ground.get_height() / 2
        )

        points_label = self.lg_font.render('POINTS', 1, Color.BLACK)

        horse = pygame.image.load(self.get_asset_path('color_unicorn.png'))
        horse = pygame.transform.scale(horse,(horse.get_width() / 3, horse.get_height() / 3))
        horse_jump = pygame.transform.rotate(horse,45)
        horse_gallop = pygame.transform.rotate(horse, -15)
        horse_dead = pygame.transform.rotate(horse,-90)

        active_horse = horse_gallop

        horse_x = display_info.current_h/3

        hurdle = pygame.image.load('./assets/images/hurdle.png')
        hurdle = pygame.transform.scale(hurdle,(hurdle.get_height()/3,hurdle.get_width()/3))

        hurdle_y = display_info.current_h - hurdle.get_height() - (2*ground.get_height()/3)

        question_board = pygame.Surface((screen_size[0]/3, screen_size[1] / 5))
        question_board = question_board.convert()
        question_board.fill(Color.WHITE)

        menu_button = Button(
            'Play',
            self.lg_font,
            Color.BLACK,
            200,
            100,
            Color.WHITE,
            Color.BLACK,
            -2
        )

        pause_label = self.lg_font.render('PAUSED',1, Color.BLACK)

        def reset():
            self.running = True
            self.playing = False
            self.gameover = False
            self.paused = False
            last_answer = -1
            question_dirty = True

            self.score = 0
            self.hurdle_number = 0
            
            self.x = -100
            self.y = 100

            self.vx = 10
            self.vy = 0

            self.direction = -1

            active_horse = horse

            horse_x = display_info.current_h/3
            

        def generate_question():
            self.question = Question()

            self.buttons[0].set_text(str(self.question.answers[0]))
            self.buttons[1].set_text(str(self.question.answers[1]))
            self.buttons[2].set_text(str(self.question.answers[2]))
            self.buttons[3].set_text(str(self.question.answers[3]))

            self.question_text_label = self.lg_font.render(str(self.question), 1, (0,0,0))
            self.hurdle_number += 1
            self.score_label = self.lg_font.render(str(self.points),1,(0,0,0))
            self.question_label = self.font.render("Hurdle #" + str(self.hurdle_number), 1, (0,0,0))
            question_board.fill((255, 255, 255))

            self.score_label = self.lg_font.render(str(self.points),1,(0,0,0))

        def set_answer(answer):
            last_answer = answer

        def evaluate_answer(answer):
            if self.question.answer == answer:
                self.points += 100
                self.score_label = self.lg_font.render(str(self.points),1,(0,0,0))
            else:
                self.set_gameover(True)

        while self.running:
            if self.playing:
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
                        elif event.key == pygame.K_r:
                            reset()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for i in range(0,3):
                            self.buttons[i].mouse_click(pygame.mouse.get_pos(),set_answer, i)

                screen_size = screen.get_size()


                if not self.paused and not self.gameover:

                    self.x += self.vx * self.direction
                    if self.direction == 1 and self.x > screen.get_width() + 50:
                        self.x = -50
                    elif self.direction == -1 and self.x < -50:
                        self.x = screen.get_width() + 50
                    self.y = display_info.current_h - horse.get_height() - ground.get_height()

                    hurdle_rect = hurdle.get_rect(topleft=(self.x,hurdle_y))
                    horse_rect = horse.get_rect(topleft=(horse_x,self.y))

                    if (active_horse == horse_jump) and (not hurdle_rect.colliderect(horse_rect)):
                        active_horse = horse

                    if (self.horse_change == self.horse_change_semaphore):
                        if (active_horse == horse):
                            active_horse = horse_gallop
                        elif (active_horse == horse_gallop):
                            active_horse = horse
                        else:
                            active_horse = horse
                        self.horse_change = 0

                    self.horse_change += 1

                    # Check if hurdle and horse in same spot.
                    if hurdle_rect.colliderect(horse_rect):
                        #evaluate answer on first frame of hurdle collision
                        if not question_dirty:
                            evaluate_answer(last_answer)
                            question_dirty = True

                        #if not gameover, jump the hurdle
                        if not self.gameover:
                            active_horse = horse_jump
                            self.y -= 200

                    #if not colliding with hurdle and question still dirty, generate new question
                    elif question_dirty:
                        generate_question()
                        question_dirty = False
                        last_answer = -1

                if self.gameover:
                    #spin the horse
                    #active_horse = pygame.transform.rotate(horse_dead, pygame.time.get_ticks())
                    active_horse = horse_dead

                # Set the "sky" color to blue
                screen.fill(background_color)

                sun = Sun()
                sun.rect.x = screen_size[1] + sun.image.get_width()
                sun.rect.y = 0

                allsprites = pygame.sprite.RenderPlain((sun))
                allsprites.draw(screen)

                screen.blit(question_board, (screen_size[0] / 4, screen_size[1] / 5))
                question_board.blit(self.question_label, (10,10))
                question_board.blit(self.question_text_label, (10,self.question_label.get_height()+10))

                screen.blit(
                    self.score_label,
                    (
                        sun.rect.x + sun.image.get_width() / 4,
                        sun.rect.y + sun.image.get_height() / 3
                    )
                )

                screen.blit(
                    points_label,
                    (
                        sun.rect.x + sun.image.get_width() / 4,
                        sun.rect.y + sun.image.get_height() / 3 + self.score_label.get_height()
                    )
                )

                screen.blit(ground, (0, screen_size[1] - ground.get_height()))
                button_panel_x = ground.get_width()/4
                button_panel_y = screen_size[1] - ground.get_height() + ground.get_height()/3+10
                screen.blit(button_panel, (button_panel_x, button_panel_y))

                self.buttons[0].rect.x = button_panel_x
                self.buttons[0].rect.y = button_panel_y
                self.buttons[0].draw(screen)

                self.buttons[1].rect.x = button_panel_x + self.buttons[0].image.get_width()
                self.buttons[1].rect.y = button_panel_y
                self.buttons[1].draw(screen)

                self.buttons[2].rect.x = button_panel_x
                self.buttons[2].rect.y = button_panel_y + self.buttons[0].image.get_height()
                self.buttons[2].draw(screen)

                self.buttons[3].rect.x = button_panel_x + self.buttons[2].image.get_width()
                self.buttons[3].rect.y = button_panel_y + self.buttons[2].image.get_height()
                self.buttons[3].draw(screen)

                screen.blit(active_horse, (horse_x, self.y))
                screen.blit(hurdle,(self.x,hurdle_y))

                # Draw the frame
                pygame.display.flip()

                # Try to stay at 30 FPS
                self.clock.tick(30)
            else:
                #in the menu
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.VIDEORESIZE:
                        pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.set_playing(True)

                screen_size = screen.get_size()
                
                screen.fill(background_color);
                
                menu_button.rect.x = (screen_size[0] - menu_button.rect.width) / 2
                menu_button.rect.y = (screen_size[1] - menu_button.rect.height) / 2
                menu_button.draw(screen)
                
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
