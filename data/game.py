## @file game.py
#  Source file for game class
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 10/14/18

import pygame, sys, random
from pygame.locals import *
from . import setup, constants, checks
from .level import Level
from .actors.text import Text
from .actors.player import Player
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
        self.enemy_count = 1
        self.player_shot_count = 1
        self.score = 0
        self.win = False
        self.quit = False
        self.checked = 0

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
        self.load_background('space')
        pygame.display.flip()

        # Start menu music
        setup.SOUNDS['OutThere'].play(-1)

        # Load logo or outcome message
        if not replay:
            game_logo = setup.IMAGES['gibbonga2']
            self.screen.blit(game_logo, (50, 75))
        else:
            self.reset_game()
            font = pygame.font.Font(setup.FONTS['arcadeclassic'], constants.MESSAGE_SIZE)
            if win:
                message = font.render("YOU  WON", True, constants.WHITE)
            else:
                message = font.render("YOU  LOST", True, constants.WHITE)
            self.screen.blit(message, (200, 200))

        # Load text
        start_game = Text("START GAME", constants.WHITE, (300, 350), self.run)
        test_game = Text("TEST GAME", constants.WHITE, (300, 400), self.test)
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



    ## Loads and blits designated background image to screen
    #  @param filename, name of background file (without extension)
    def load_background(self, filename):
        background_img = setup.IMAGES[filename]
        background = pygame.Surface(constants.SCREENRECT.size)
        for x in range(0, constants.SCREENRECT.width, background_img.get_width()):
            background.blit(background_img, (x, 0))
        self.screen.blit(background, (0, 0))
        return background

    ## Remove dead actors and out-of-frame actors
    #  @param actors, array with actors to be checked for removal
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
        background = self.load_background('space')
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

    ## Runs a test game session
    #  @pre: Game components have been initialized
    #  @post: Test results have been printed to terminal
    def test(self):
        ##CHECK
        #checking if the mixer is correctly initialized
        mixer_check = pygame.mixer.get_init()
        if mixer_check == None:
            self.checked += 1
            checks.MIXER_INITIALIZED = False
        else:
            self.checked += 1
            checks.CHECK_7 = True

        # Load background
        background = self.load_background('space')
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

        #Moved the initial starting postion out of the loop and controlling back and forth
        x_dir = constants.SCREENRECT.centerx
        hit_right = True
        hit_left = False

        # Game loop
        while player.alive and not self.win and not self.quit:

            self.clock.tick(constants.FPS)

            # Call event queue
            pygame.event.pump()

            # Process input
            key_presses = pygame.key.get_pressed()
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

            # Move the player, x_dir initialization moved outside while loop with a starting value of the center.
            #Uses hit_right and hit_left to tell if the edges have been hit.
            if player.rect.x < 50:
                hit_left = True
                hit_right = False
            if player.rect.x > 500:
                hit_left = False
                hit_right = True

            if hit_right:
                x_dir = - 1
                player.move(x_dir)
            elif hit_left:
                x_dir = + 1
                player.move(x_dir)

            # Update text
            score_text.update_text("Score " + str(self.score))
            level_text.update_text("Level " + str(level.level))

            # Spawn player shots
            shots_check = len(shots)
            if not int(random.random()* constants.PLAYER_SHOT_ODDS):
                if len(shots) < constants.MAX_SHOTS:
                    self.player_shot_count += 1
                    shots.append(Shot(player))
                    setup.SOUNDS['shot'].play()
                    ##CHECK
                    #increment check count
                    if not checks.CHECK_6:
                        checks.CHECK_6 = True
                        self.checked += 1
                    if len(shots) == (shots_check+1):
                        checks.PLAYER_SHOT_LIST_INCREMENTS = True
                    else:
                        checks.PLAYER_SHOT_LIST_INCREMENTS = False

            # Make enemies shoot
            if len(enemies) > 0:
                ##CHECK
                ##make sure the enemy_shot array is incrementing
                check = len(enemy_shots)
                if not int(random.random() * constants.ENEMY_SHOT_ODDS):
                    if self.enemy_shot_count < constants.MAX_ENEMY_SHOT:
                        self.enemy_shot_count += 1
                        enemy_shots.append(Enemy_shot(enemies[random.randint(0, len(enemies)-1)]))
                        ##CHECK
                        #increment check count
                        if not checks.CHECK_1:
                            checks.CHECK_1 = True
                            self.checked += 1
                        if len(enemy_shots) == (check+1):
                            checks.ENEMY_SHOT_LIST_INCREMENTS = True
                        else :
                            checks.ENEMY_SHOT_LIST_INCREMENTS = False
                            print("Enemy_shot list increments when enemy shoots: FALSE")
                        #CHECK to make sure enemies not spawning when MAX_ENEMIES is reached
                        #increment check count
                        if not checks.CHECK_2:
                            checks.CHECK_2 = True
                            self.checked += 1
                        if self.enemy_shot_count > constants.MAX_ENEMY_SHOT:
                            checks.LESS_MAX_ENEMY_SHOT = False
                            print("Enemies stop shooting when max count reached: FALSE")

            # Spawn recovery health objects
            if player.health < 3:
                if random.randint(1, 201) == 1:
                    recover_health.append(Recover_health())
                    #check that health is not going over 3
                    #increment check count
                    if not checks.CHECK_3:
                        checks.CHECK_3 = True
                        self.checked += 1
                    if player.health > 3:
                        checks.MAX_HEALTH = False

            # Check for player power ups
            for powerup in recover_health:
                #check to make sure health increments when collides with player
                checkLen = player.health
                if powerup.collide_with(player):
                    player.recover()
                    #increment check count
                    if not checks.CHECK_4:
                        checks.CHECK_4 = True
                        self.checked += 1
                    if player.health != checkLen + 1:
                        checks.HEALTH_MORE = False
                    #check make sure health does not go over 3
                    if player.health > 3:
                        checks.MAX_HEALTH = False

            # Check for player hits
            for threat in enemies + enemy_shots:
                if threat.collide_with(player):
                    if player.health == 1 and self.checked != checks.NUM_CHECKS:
                        print("Three additional health added to meet all checks")
                        player.health = 3
                    else:
                        #check to make sure health decrements when player is hit
                        checkLen = player.health
                        player.hit()
                        #increment check count
                        if not checks.CHECK_5:
                            checks.CHECK_5 = True
                            self.checked += 1
                            if player.health != checkLen -1:
                                checks.HEALTH_HIT = False

            ##CHECK
            #check if enemy go outside the screen edges
            enemies_over_edges_l = False
            enemies_over_edges_r = False
            if not checks.CHECK_8:
                checks.CHECK_8 = True
                self.checked += 1
                for enemy in enemies:
                    if enemy.rect.left <= constants.SCREENRECT.left:
                        enemies_over_edges_l = True
                    if enemy.rect.right >= constants.SCREENRECT.right:
                        enemies_over_edges_r = True
                if enemies_over_edges_l or enemies_over_edges_r:
                    checks.ENEMIES_OVER_EDGES = False

            ##CHECK
            #check if player go outside the screen edges
            over_edges_l = False
            over_edges_r = False
            if not checks.CHECK_9:
                checks.CHECK_9 = True
                self.checked += 1
                if player.rect.left <= constants.SCREENRECT.left:
                    over_edges_l = True
                if player.rect.right >= constants.SCREENRECT.right:
                    over_edges_r = True
            if over_edges_l or over_edges_r:
                checks.PLAYER_OVER_EDGES = False

            # Check for enemy kills
            enemies_detection = 0
            score_increment = 0
            for enemy in enemies:
                for shot in shots:
                    if shot.collide_with(enemy):
                        setup.SOUNDS['enemy'].play()
                        enemy.die()
                        enemies_detection += 1
                        score_increment += 1
                        self.score += 1

            ##CHECK
            #Check if score increases by one with each enemy killed
            if not checks.CHECK_10:
                checks.CHECK_10 = True
                self.checked += 1
                if enemies_detection != score_increment:
                    checks.SCORE_INCREMENT = False

            # Draw actors
            for actor in [player] + [health] + text + enemies + shots + enemy_shots + recover_health:
                render = actor.draw(self.screen)
                actors.append(render)

            # Update actors
            pygame.display.update(actors)
            actors = []

            # Check win
            self.win = level.game_win(self.score)

        #CHECKS
        print("----------------------------------------------------------------------")
        print("Number of checks: " + str(checks.NUM_CHECKS))
        print("Number of checks checked: " + str(self.checked))
        print("----------------------------------------------------------------------")
        print("TEST 1:  Mixer is initialized: " + str(checks.MIXER_INITIALIZED))
        print("Test 2:  Score increases correctly: " + str (checks.SCORE_INCREMENT))
        print("Test 3:  Enemies dont go over edges: " + str(checks.ENEMIES_OVER_EDGES))
        print("Test 4:  Player does not go over edges: " + str(checks.PLAYER_OVER_EDGES))
        print("Test 5:  Does not go over max enemy: " + str(checks.LESS_MAX_ENEMIES))
        print("Test 6:  List increments when enemy shoots: " + str(checks.ENEMY_SHOT_LIST_INCREMENTS))
        print("Test 7:  List increments when player shoots: " + str(checks.PLAYER_SHOT_LIST_INCREMENTS))
        print("Test 8:  Player health does not go over three: " + str(checks.MAX_HEALTH))
        print("Test 9:  Player health increments if catches heart: " + str(checks.HEALTH_MORE))
        print("Test 10: Player health decrements when player is hit: " + str(checks.HEALTH_HIT))
        print("----------------------------------------------------------------------")

        # Exit game, sound, and system
        setup.SOUNDS['background'].stop()
        pygame.time.delay(250)
        if not player.alive:
            setup.SOUNDS['gameover'].play()
            self.menu(True, False)
        elif self.win:
            self.menu(True, True)

    ## Resets the game before replay
    #  @post Set game constants back to original values
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
