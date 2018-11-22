## @file game.py
#  Source file for game class
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 10/14/18

import pygame, sys, random
from pygame.locals import *
from . import setup, constants
from .level import Level
from .actors.text import Text
from .actors.player import Player
from .actors.enemy import Enemy
from .actors.shot import Shot
from .actors.health import Health
from .actors.enemy_shot import Enemy_shot
from .actors.recover_health import Recover_health


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
        self.screen = pygame.display.set_mode(constants.SCREENRECT.size, 0)
        self.clock = pygame.time.Clock()
        self.enemy_shot_count = 1
        self.score = 0
        self.win = False
        self.quit = False

        # Setup Game Window
        icon = setup.IMAGES['starship']
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Gibbonga')
        #pygame.mouse.set_visible(0)

        self.menu()

    ## Loads a start screen with clickable options
    #  @pre Game components have been initialized
    #  @param replay, True for replay screen [OPTIONAL]
    #  @param win, True if user won previous game [OPTIONAL]
    def menu(self, replay=False, win=False):

        # Load background
        self.load_background()
        pygame.display.flip()

        # Start menu music
        setup.SOUNDS['OutThere'].play(-1)

        # Load logo or outcome message
        if not replay:
            game_logo = setup.IMAGES['gibbonga2']
            self.screen.blit(game_logo, (50, 75))
        else:
            self.reset_game()
            font = pygame.font.Font(constants.GAME_FONT, constants.MESSAGE_SIZE)
            if win:
                message = font.render("YOU  WON", True, constants.WHITE)
            else:
                message = font.render("YOU  LOST", True, constants.WHITE)
            self.screen.blit(message, (200, 200))

        # Load text
        start_game = Text("START GAME", constants.WHITE, (300, 350), self.run)
        test_game = Text("TEST GAME", constants.WHITE, (300, 400))
        quit_game = Text("QUIT GAME", constants.WHITE, (300, 450), self.quit_game)

        # Draw text on screen
        menu_text = []
        for text in [start_game] + [test_game] + [quit_game]:
            render = text.draw(self.screen)
            menu_text.append(render)
        pygame.display.update(menu_text)

        exit_menu = False
        while not exit_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for text in [start_game] + [test_game] + [quit_game]:
                        if text.rect.collidepoint(pos):
                            setup.SOUNDS['OutThere'].stop()
                            exit_menu = True
                            text.action()

    def load_background(self):
        background_img = setup.IMAGES['space']
        background = pygame.Surface(constants.SCREENRECT.size)
        for x in range(0, constants.SCREENRECT.width, background_img.get_width()):
            background.blit(background_img, (x, 0))
        self.screen.blit(background, (0, 0))
        return background

    def clean(self, actors):
        for actor in actors:
            if actor.rect.top <= 0 or actor.rect.bottom >= constants.SCREENRECT.height or not actor.alive:
                actors.remove(actor)
        return actors


    ## Runs the game session
    #  @pre: Game components have been initialized
    #  @post: Game has been exited properly
    def run(self):

        # Load background
        background = self.load_background()
        pygame.display.flip()

        # Start background music
        setup.SOUNDS['background'].play(-1)

        # Initialize starting actors
        player = Player()
        health = Health(player)
        recover_health = []
        shots = []
        enemy_shots = []
        enemies = []
        text = []

        # Initialize on-screen score
        score_text = Text("Score 0", constants.WHITE, (75, 25))
        text.append(score_text)

        # Initialize on-screen level counter
        level_text = Text("", constants.WHITE, (500, 25))
        text.append(level_text)

        # Initialize array for updating actors
        actors = []

        # Initialize level manager
        level = Level()

        # Game loop
        while player.alive and not self.win and not self.quit:

            self.clock.tick(constants.FPS)

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
                self.quit_game()

            # Update level upon pass
            if level.pass_level(self.score):
                level.next_level()
                enemies = enemies + level.generate_enemies()

            # Update enemies
            level.update(enemies)

            # Clear screen and update actors
            for actor in [player] + [health] + text + enemies + shots + enemy_shots + recover_health:
                render = actor.erase(self.screen, background)
                actors.append(render)
                actor.update()

            # Remove out-of-frame objects
            for dead_actors in [shots] + [enemy_shots] + [enemies] + [recover_health]:
                self.clean(dead_actors)

            # Move the player
            x_dir = right - left
            player.move(x_dir)

            # Update text
            score_text.update_text("Score " + str(self.score))
            level_text.update_text("Level " + str(level.level))

            # Spawn player shots
            if not player.reloading and shoot and len(shots) < constants.MAX_SHOTS:
                shots.append(Shot(player))
                setup.SOUNDS['shot'].play()
            player.reloading = shoot

            # Spawn enemy shots
            if len(enemies) > 0 and self.enemy_shot_count < constants.MAX_ENEMY_SHOT:
                if not int(random.random() * constants.ENEMY_SHOT_ODDS):
                    self.enemy_shot_count += 1
                    enemy_shots.append(Enemy_shot(enemies[random.randint(0, len(enemies) - 1)]))

            # Spawn recovery health objects
            if player.health < 3:
                if random.randint(1, 201) == 1:
                    recover_health.append(Recover_health())

            # Check for player power ups
            for powerup in recover_health:
                if powerup.collide_with(player):
                    player.recover()

            # Check for player hits
            for threat in enemies + enemy_shots:
                if threat.collide_with(player):
                    player.hit()

            # Check for enemy kills
            for enemy in enemies:
                for shot in shots:
                    if shot.collide_with(enemy):
                        setup.SOUNDS['enemy'].play()
                        enemy.die()
                        self.score += 1

            # Draw actors
            for actor in [player] + [health] + text + enemies + shots + enemy_shots + recover_health:
                render = actor.draw(self.screen)
                actors.append(render)

            # Update actors
            pygame.display.update(actors)
            actors = []

            # Check win
            self.win = level.game_win(self.score)

        # Exit game, sound, and system
        setup.SOUNDS['background'].stop()
        pygame.time.delay(250)
        if not player.alive:
            setup.SOUNDS['gameover'].play()
            self.menu(True, False)
        elif self.win:
            self.menu(True, True)

    def reset_game(self):
        self.enemy_shot_count = 1
        self.score = 0
        self.win = False

    ## Quits the game
    #  @pre A game session is running
    #  @post All components have been properly suspended
    def quit_game(self):
        pygame.time.delay(250)
        pygame.display.quit()
        pygame.quit()
        sys.exit()
