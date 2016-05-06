#!/usr/bin/env python2

import pygame
import random
import os
import math

from sprites.sun import Sun
from sprites.horse import Horse
from objects.button import Button
from question import Question
from fractions import Fraction

class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    SKYBLUE = (126, 192, 238)
    BROWN = (127, 96, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

class MathHurdler:
    def __init__(self):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()

        self.x = -100
        self.vx = 10

        self.paused = False
        self.direction = -1

        self.circle_size = 150

        self.horse_change_semaphore = 3
        self.horse_change = 0

        self.font = pygame.font.SysFont('monospace', 36)
        self.lg_font = pygame.font.SysFont('monospace', 60)
        self.xlg_font = pygame.font.SysFont('monospace', 90)

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

        self.songs = [
            self.get_sound_path('william_tell_overture_intro.wav'),
            self.get_sound_path('william_tell_overture_race.wav')
        ]

        self.death_sfx = pygame.mixer.Sound(self.get_sound_path('sad_trombone.wav'))
        self.jump_sfx = pygame.mixer.Sound(self.get_sound_path('success.wav'))

    def set_paused(self, paused):
        self.paused = paused
        if paused:
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.play(-1)

    def set_gameover(self, gameover):
        self.gameover = gameover
        if gameover:
            pygame.mixer.music.stop()
            self.death_sfx.play()

    def set_playing(self, playing):
        self.playing = playing
        self.set_paused(False)
        self.set_gameover(False)
        if playing:
            pygame.mixer.music.load(self.songs[1])
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.load(self.songs[0])
            pygame.mixer.music.play(-1)

    def get_image_path(self, asset_name):
        return os.path.join('./assets/images', asset_name)

    def get_sound_path(self, sound_name):
        return os.path.join('./assets/sounds', sound_name)

    # The main game loop.
    def run(self):
        self.running = True
        self.playing = False
        self.gameover = False
        self.paused = False
        self.last_answer = -1
        self.last_answer_index = -1
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
                str(self.question.choices[i]),
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

        sun = Sun()
        sun.rect.topleft = (screen_size[0]- sun.image.get_width(),0)

        horse = Horse()
        horse.rect.x = display_info.current_h/3
        horse.rect.y = display_info.current_h - horse.image.get_height() - ground.get_height()

        hurdle = pygame.image.load('./assets/images/hurdle.png')
        hurdle = pygame.transform.scale(hurdle,(hurdle.get_height()/3,hurdle.get_width()/3))

        hurdle_y = display_info.current_h - hurdle.get_height() - (2*ground.get_height()/3)

        question_board = pygame.Surface((screen_size[0]/3, screen_size[1] / 5))
        question_board = question_board.convert()
        question_board.fill(Color.WHITE)

        play_button = Button(
            'Play',
            self.lg_font,
            Color.BLACK,
            200,
            100,
            Color.WHITE,
            Color.BLACK,
            -2
        )

        menu_label = self.xlg_font.render('MATH HURDLER', 1, Color.BLACK)
        gameover_label = self.xlg_font.render('GAME OVER', 1, Color.BLACK)

        pygame.mixer.music.load(self.songs[0])
        pygame.mixer.music.play(-1)

        def reset():
            question_dirty = True

            self.score = 0
            self.hurdle_number = 0
            
            self.x = -100
            self.vx = 10

            self.direction = -1

            horse.set_horse(Horse.BASE)

            set_answer(-1)

        def generate_question():
            self.question.next()

            self.buttons[0].set_text(str(self.question.choices[0]))
            self.buttons[1].set_text(str(self.question.choices[1]))
            self.buttons[2].set_text(str(self.question.choices[2]))
            self.buttons[3].set_text(str(self.question.choices[3]))

            self.buttons[0].set_color(self.buttons[0].color, False)
            self.buttons[1].set_color(self.buttons[0].color, False)
            self.buttons[2].set_color(self.buttons[0].color, False)
            self.buttons[3].set_color(self.buttons[0].color, False)

            self.question_text_label = self.lg_font.render(str(self.question), 1, Color.BLACK)
            self.hurdle_number += 1
            self.score_label = self.lg_font.render(str(self.points),1,Color.BLACK)
            self.question_label = self.font.render("Hurdle #" + str(self.hurdle_number), 1, Color.BLACK)
            question_board.fill(Color.WHITE)

            self.score_label = self.lg_font.render(str(self.points), 1, Color.BLACK)

        def set_answer(answer_index):
            #unselect the previous answer button
            if self.last_answer_index >= 0:
                self.buttons[self.last_answer_index].set_selected(False)
            
            if answer_index >= 0:
                self.last_answer = Fraction(self.buttons[answer_index].text)
                self.buttons[answer_index].set_selected(True)
                self.last_answer_index = answer_index
            else:
                self.last_answer = -1
                self.last_answer_index = -1
            

        def evaluate_answer(answer):
            if self.question.is_answer(answer):
                self.points += 100
                self.score_label = self.lg_font.render(str(self.points), 1, Color.BLACK)
                self.jump_sfx.play()
            else:
                self.set_gameover(True)
                if self.last_answer_index >= 0:
                    self.buttons[self.last_answer_index].set_color(Color.RED, False)
                
            self.buttons[self.question.answer_index].set_color(Color.GREEN, False)

        while self.running:
            if self.playing:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.VIDEORESIZE:
                        pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.paused = not self.paused
                        elif event.key == pygame.K_r:
                            reset()
                            self.set_playing(False)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if not self.gameover:
                            for i in range(0, 4):
                                self.buttons[i].mouse_click(
                                    pygame.mouse.get_pos(),
                                    set_answer,
                                    i
                                )

                screen_size = screen.get_size()

                if not self.paused and not self.gameover:

                    self.x += self.vx * self.direction
                    if self.direction == 1 and self.x > screen.get_width() + 50:
                        self.x = -50
                    elif self.direction == -1 and self.x < -50:
                        self.x = screen.get_width() + 50

                    hurdle_rect = hurdle.get_rect(topleft=(self.x,hurdle_y))

                    if (horse.active_horse == Horse.JUMP) and (not horse.rect.colliderect(hurdle_rect)):
                        horse.set_horse(Horse.BASE)
                    if (self.horse_change == self.horse_change_semaphore):
                        horse.gallop()
                        self.horse_change = 0

                    self.horse_change += 1

                    horse.rect.x = display_info.current_w / 3
                    horse.rect.y = display_info.current_h - hurdle.get_height() - (3*ground.get_height()/4)

                    # Check if hurdle and horse in same spot.
                    if horse.rect.colliderect(hurdle_rect):
                        #evaluate answer on first frame of hurdle collision
                        if not question_dirty:
                            evaluate_answer(self.last_answer)
                            question_dirty = True

                        #if not gameover, jump the hurdle
                        if not self.gameover:
                            horse.set_horse(Horse.JUMP)
                            horse.rect.x = display_info.current_w / 3
                            horse.rect.y = display_info.current_h - horse.image.get_height() - ground.get_height() - 100

                    #if not colliding with hurdle and question still dirty, generate new question
                    elif question_dirty:
                        generate_question()
                        question_dirty = False
                        set_answer(-1)

                if self.gameover:
                    #spin the horse
                    horse.set_horse(Horse.DEAD)

                # Set the "sky" color to blue
                screen.fill(background_color)
                
                sun.rect.topleft = (screen_size[0]- sun.image.get_width(),0)

                screen.blit(question_board, (screen_size[0] / 4, screen_size[1] / 5))
                question_board.blit(self.question_label, (10,10))
                question_board.blit(self.question_text_label, (10,self.question_label.get_height()+10))

                screen.blit(ground, (0, screen_size[1] - ground.get_height()))
                button_panel_x = ground.get_width()/4
                button_panel_y = screen_size[1] - ground.get_height() + ground.get_height() / 3 + 10
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

                screen.blit(hurdle,(self.x,hurdle_y))

                allsprites = pygame.sprite.RenderPlain(sun,horse)
                allsprites.draw(screen)

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

                if self.gameover:
                    screen.blit(
                        gameover_label,
                        (
                            (screen_size[0] - gameover_label.get_width()) / 2,
                            (screen_size[1] - gameover_label.get_height()) / 2,
                        )
                    )

                # Draw the frame
                pygame.display.flip()

                if self.gameover:
                    pygame.time.wait(6000)
                    self.set_playing(False)
                    reset()

                # Try to stay at 30 FPS
                self.clock.tick(30)
                
            else:
                def start_game():
                    reset()
                    self.set_playing(True)

                #in the menu
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.VIDEORESIZE:
                        pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.set_playing(True)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        play_button.mouse_click(
                            pygame.mouse.get_pos(),
                            start_game
                        )

                screen_size = screen.get_size()

                if (self.horse_change == self.horse_change_semaphore):
                    horse.gallop()
                    self.horse_change = 0

                self.horse_change += 1

                #draw rainbow background fill
                screen.fill(
                    (
                        math.floor(math.sin(pygame.time.get_ticks()*.001)*55 + 200),
                        math.floor(math.sin(pygame.time.get_ticks()*.001+math.pi)*55 + 200),
                        math.floor(math.sin(pygame.time.get_ticks()*.001+math.pi*.5)*55 + 200)
                    )
                )

                #draw menu horse
                horse.rect.x = (screen_size[0] - horse.image.get_width()) / 2
                horse.rect.y = (screen_size[1] - horse.image.get_height()) / 2 + 200

                menu_sprites = pygame.sprite.RenderPlain(horse)
                menu_sprites.draw(screen)

                #draw play button
                play_button.rect.x = (screen_size[0] - play_button.rect.width) / 2
                play_button.rect.y = (screen_size[1] - play_button.rect.height) / 2
                play_button.draw(screen)

                #draw menu label
                screen.blit(
                    menu_label,
                    (
                        (screen_size[0] - menu_label.get_width()) / 2,
                        (screen_size[1] - menu_label.get_height()) / 2 - 200,
                    )
                )
                
                
                
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
