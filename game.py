## @file game.py
#  Source file for game class
#
#  Project: Gallaga Clone
#  Author: Py Five
#  Created: 10/14/19

import pygame
import os.path
import sys
import random
from player import Player
from enemy import Enemy
from shot import Shot
from health import Health
from pygame.locals import *
import constants as const


## @class Game
#  @brief Runs the game session and manages all actors
class Game:

    ## Constructor
    #  @post: Game components have been initialized
    def __init__(self):

        # Initialize pygame
        pygame.init()

        # Initialize member variables
        self.screen = pygame.display.set_mode(const.SCREENRECT.size, 0)
        self.clock = pygame.time.Clock()
        self.quit = False
        self.enemy_count = 0

        # Setup Game Window
        icon = pygame.image.load('assets/images/player_ship.png')
        icon = pygame.transform.scale(icon, (60, 80))
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Gallaga Clone')
        pygame.mouse.set_visible(0)


    ## Loads and scales object/game image
    #  @author: Kristi
    #  @pre: image exists
    #  @param: filename, name of image to be loaded
    #  @param: width, desired width of image
    #  @param: height, desired height of image
    #  @returns: Surface object
    def load_image(self, filename, file_width, file_height):

        # Load image
        filename = os.path.join('assets/images', filename)
        img = pygame.image.load(filename)

        # Scale image
        img = pygame.transform.scale(img, (file_width, file_height))

        # Make transparent
        img.set_colorkey(img.get_at((0,0)), RLEACCEL)

        return img.convert()

    # def update_health(self, player):
    #     if player.health == 0:
    #         player.alive = False
    #     elif player.health == 1:
    #
    #     elif player.health == 2:



    ## Runs the game session
    #  @pre: Game components have been initialized
    #  @post: Game has been exited properly
    def run(self):

        # Load Images
        background_img = pygame.image.load('assets/images/space.jpg')
        player_img = self.load_image('player_ship.png', 45, 65)
        enemy_img = self.load_image('enemy_spaceship.png', 26, 26)
        shot_img = self.load_image('missile1.png', 10, 24)
        health_img_3 = self.load_image('hearts_3.png', 60, 20)
        health_img_2 = self.load_image('hearts_2.png', 60, 20)
        health_img_1 = self.load_image('hearts_1.png', 60, 20)
        health_img_0 = self.load_image('hearts_0.png', 60, 20)

        # Load Background
        background = pygame.Surface(const.SCREENRECT.size)
        for x in range(0, const.SCREENRECT.width, background_img.get_width()):
            background.blit(background_img, (x, 0))
        self.screen.blit(background, (0, 0))
        pygame.display.flip()

        # Initialize Starting Actors
        player = Player(player_img)
        health = Health(health_img_3, player)
        enemies = [Enemy(enemy_img)]
        shots = []
        actors = []


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

            # Update actors
            for actor in [player] + [health] + enemies + shots:
                render = actor.erase(self.screen, background)
                actors.append(render)
                actor.update()

            # Remove out-of-frame shots
            for shot in shots:
                if shot.rect.top <= 0:
                    shots.remove(shot)

            # Move the player
            x_dir = right - left
            player.move(x_dir)

            # Create new shots
            if not player.reloading and shoot and len(shots) < const.MAX_SHOTS:
                shots.append(Shot(shot_img, player))
            player.reloading = shoot

            # Create new alien
            if not int(random.random() * const.ENEMY_ODDS):
                #counting the number of enemies that were spawned
                self.enemy_count += 1
                #only appends until the number of max is reached
                if(self.enemy_count < const.MAX_ENEMIES):
                    enemies.append(Enemy(enemy_img))

            # Check for collisions
            for enemy in enemies:
                if enemy.collision_check(player):
                    enemies.remove(enemy)
                    player.health -= 1
                    if player.health == 0:
                        health.image = health_img_0
                        player.alive = False
                    elif player.health == 1:
                        health.image = health_img_1
                    elif player.health == 2:
                        health.image = health_img_2

                #enemies go away once they hit the bottom
                if enemy.rect.y >= const.SCREENRECT.height - 30:
                    enemies.remove(enemy)

                for shot in shots:
                    if shot.collision_check(enemy):
                        enemies.remove(enemy)

            # Draw actors
            for actor in [player] + [health] + enemies + shots:
                render = actor.draw(self.screen)
                actors.append(render)

            # Update actors
            pygame.display.update(actors)
            actors = []

        # Exit game and system
        pygame.display.quit()
        pygame.quit()
        sys.exit()
