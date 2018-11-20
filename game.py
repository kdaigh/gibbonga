## @file game.py
#  Source file for game class
#
#  Project: Gallaga Clone
#  Author: Py Five
#  Created: 10/14/19

import pygame
import sys
import random
from text import Text
from player import Player
from enemy import Enemy
from shot import Shot
from health import Health
from pygame.locals import *
import constants as const
from enemy_shot import Enemy_shot
from recover_health import Recover_health
import setup


## @class Game
#  @brief Runs the game session and manages all actors
class Game:

    ## Constructor
    #  @post: Game components have been initialized
    def __init__(self):

        # Initialize pygame
        pygame.init()
        pygame.mixer.init()

        # Initialize member variables
        self.screen = pygame.display.set_mode(const.SCREENRECT.size, 0)
        self.clock = pygame.time.Clock()
        self.quit = False
        self.enemy_count = 1
        self.enemy_shot_count = 1
        self.gameover = False
        self.score = 0

        # Setup Game Window
        icon = pygame.image.load('assets/images/player_ship.png')
        icon = pygame.transform.scale(icon, (60, 80))
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Gallaga Clone')
        #pygame.mouse.set_visible(0)

        self.menu()

    ## Loads a start screen with clickable options
    #  @pre Game components have been initialized
    def menu(self):
        # Load black background
        self.screen.fill(const.BLACK)
        pygame.display.update()

        # Load text
        start_game = Text("START GAME", const.WHITE, (300, 100), self.run)
        test_game = Text("TEST GAME", const.WHITE, (300, 200))
        quit_game = Text("QUIT GAME", const.WHITE, (300, 300), self.quit_game)

        # Draw text on screen
        options = []
        for text in [start_game] + [test_game] + [quit_game]:
            render = text.draw(self.screen)
            options.append(render)

        # Draw screen
        pygame.display.update(options)

        exit_menu = False
        while not exit_menu:
            for event in pygame.event.get():
                if pygame.event.peek(QUIT):
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for text in [start_game] + [test_game] + [quit_game]:
                        if text.rect.collidepoint(pos):
                            exit_menu = True
                            text.action()

    def load_background(self):
        background_img = setup.IMAGES['space']
        background = pygame.Surface(const.SCREENRECT.size)
        for x in range(0, const.SCREENRECT.width, background_img.get_width()):
            background.blit(background_img, (x, 0))
        self.screen.blit(background, (0, 0))
        return background

    def clean(self, actors):
        for actor in actors:
            if actor.rect.top <= 0 or actor.rect.bottom >= const.SCREENRECT.height or not actor.alive:
                actors.remove(actor)
        return actors


    ## Runs the game session
    #  @pre: Game components have been initialized
    #  @post: Game has been exited properly
    def run(self):

        # Load background
        background = self.load_background()
        pygame.display.flip()

        # Load and play background music
        pygame.mixer.music.load('assets/audios/background.wav')
        pygame.mixer.music.play(20)

        # Initialize Starting Actors
        player = Player()
        health = Health(player)
        recover_health = []
        enemies = [Enemy()]
        shots = []
        enemy_shots = []
        actors = []
        score_text = Text("Score 0", const.WHITE, (50, 25))

        # Game loop
        while player.alive and not self.quit:

            self.clock.tick(const.FPS)

            # Call event queue
            pygame.event.pump()

            # Process input
            key_presses = pygame.key.get_pressed()
            right = key_presses[pygame.K_RIGHT]
            left = key_presses[pygame.K_LEFT]
            shoot = key_presses[pygame.K_SPACE]
            exit = key_presses[pygame.K_q]

            # Check for quit conditions
            if pygame.event.peek(QUIT) or exit:
                self.quit = True
                break

            # Clear screen and update actors
            for actor in [score_text] + [player] + [health] + enemies + shots + enemy_shots + recover_health:
                render = actor.erase(self.screen, background)
                actors.append(render)
                actor.update()

            # Remove out-of-frame objects
            # Testing code -- If this breaks, use "self.clean_objects(...) for each
            for dead_actors in [shots] + [enemy_shots] + [enemies] + [recover_health]:
                self.clean(dead_actors)

            # Move the player
            x_dir = right - left
            player.move(x_dir)

            # Update text
            score_text.update_text("Score " + str(self.score))

            # Spawn player shots
            if not player.reloading and shoot and len(shots) < const.MAX_SHOTS:
                shots.append(Shot(player))
                setup.SOUNDS['shot'].play()
            player.reloading = shoot

            # Spawn enemy
            if not int(random.random() * const.ENEMY_ODDS):
                if self.enemy_count < const.MAX_ENEMIES:
                    self.enemy_count += 1
                    enemies.append(Enemy())

            # Spawn enemy shot
            if not int(random.random() * const.ENEMY_SHOT_ODDS):
                if len(enemies) > 0 and self.enemy_shot_count < const.MAX_ENEMY_SHOT:
                    self.enemy_shot_count += 1
                    enemy_shots.append(Enemy_shot(enemies[random.randint(0, len(enemies) - 1)]))

            # Spawn recovery health objects
            if player.health < 3:
                if random.randint(1, 201) == 1:
                    recover_health.append(Recover_health())

            # Check for player hits
            for threat in enemies + enemy_shots:
                if threat.collide_with(player):
                    player.hit()

            # Check for player power ups
            for health in recover_health:
                if health.collide_with(player):
                    player.recover()

            # Check for player kills
            for enemy in enemies:
                for shot in shots:
                    if shot.collide_with(enemy):
                        setup.SOUNDS['enemy'].play()
                        enemies.remove(enemy)
                        self.score += 1

            # Draw actors
            for actor in [score_text] + [player] + [health] + enemies + shots + enemy_shots + recover_health:
                render = actor.draw(self.screen)
                actors.append(render)

            # Update actors
            pygame.display.update(actors)
            actors = []

        # Exit game and system
        if not player.alive:
            setup.SOUNDS['gameover'].play()
        self.quit_game()

    ## Quits the game
    #  @pre A game session is running
    #  @post All components have been properly suspended
    def quit_game(self):
        pygame.time.delay(2000)
        pygame.display.quit()
        pygame.quit()
        sys.exit()
