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
from enemy_shot import Enemy_shot
from recover_health import Recover_health


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
        self.enemy_shot_count = 0
        self.gameover = False
        self.score = 0

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

        #Load audios
    def load_audio(self, filename):

        sound = pygame.mixer.Sound('assets/audios/'+filename)
        return sound

    def keep_score(self, surface, text, text_size, x, y):
        #setting font
        font = pygame.font.SysFont("arial", text_size)
        #rendering text
        score_surface = font.render(text, True, (255, 255, 255))
        #blitting to screen
        surface.blit(score_surface, (x, y))
        #trying to update
        pygame.display.update()


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
        enemy_shot_img = self.load_image('missile2.png', 10, 24)
        recover_health_img = self.load_image('hearts_1.png', 60, 20)

        # Load Background
        background = pygame.Surface(const.SCREENRECT.size)
        for x in range(0, const.SCREENRECT.width, background_img.get_width()):
            background.blit(background_img, (x, 0))
        self.screen.blit(background, (0, 0))
        pygame.display.flip()

        # load audio:
        shot_audio = self.load_audio('shot.wav')
        explode_audio = self.load_audio('explosion.wav')
        enemy_audio = self.load_audio('enemy.wav')
        gameover_audio = self.load_audio('gameover.wav')
        hit_audio = self.load_audio('hit.wav')
        # Should be music not sound
        #main_menu_audio = self.load_audio('main_menu.mp3')

        # Load and play background music
        pygame.mixer.music.load('assets/audios/background.wav')
        pygame.mixer.music.play(20)

        # Initialize Starting Actors
        player = Player(player_img)
        health = Health(health_img_3, player)
        recover_health = []
        enemies = [Enemy(enemy_img)]
        shots = []
        enemy_shots = []
        actors = []

        # Game loop
        while player.alive and not self.quit:

            self.clock.tick(const.FPS)

            # Call event queue
            pygame.event.pump()

            # calling keep score
            self.keep_score(self.screen, "Score: " + str(self.score), 20, 20, 20)

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
            for actor in [player] + [health] + enemies + shots + enemy_shots + recover_health:
                render = actor.erase(self.screen, background)
                actors.append(render)
                actor.update()

            # Remove out-of-frame shots
            for shot in shots:
                if shot.rect.top <= 0:
                    shots.remove(shot)

            for shot in enemy_shots:
                if shot.rect.bottom >= const.SCREENRECT.height:
                    enemy_shots.remove(shot)

            # Move the player
            x_dir = right - left
            player.move(x_dir)

            # Create new shots
            if not player.reloading and shoot and len(shots) < const.MAX_SHOTS:
                shots.append(Shot(shot_img, player))
                shot_audio.play()
            player.reloading = shoot

            # Create new alien
            if not int(random.random() * const.ENEMY_ODDS):
                #only appends until the number of max is reached
                if(self.enemy_count < const.MAX_ENEMIES):
                    #counting the number of enemies that were spawned
                    self.enemy_count += 1
                    enemies.append(Enemy(enemy_img))

            #spawning health recovery objects on screen
            if player.health < 3:
                if random.randint(1, 201) == 1:
                    recover_health.append(Recover_health(recover_health_img))

            #player collision with health recovery objects
            for z in recover_health:
                if player.health < 3:
                    if z.pickup(player):
                        recover_health.remove(z)
                        player.health += 1
                        if player.health == 3:
                            health.image = health_img_3
                        elif player.health == 2:
                            health.image = health_img_2

            #remove health recovery object as it moves off screen
            for z in recover_health:
                if z.rect.bottom >= const.SCREENRECT.height:
                    recover_health.remove(z)

            # Make enemies shoot
            #i = 0
            #for x in enemies:
            if not int(random.random() * const.ENEMY_SHOT_ODDS):
                self.enemy_shot_count += 1
                if (self.enemy_shot_count < const.MAX_ENEMY_SHOT):
                    #enemy_shots.append(Enemy_shot(enemy_shot_img, enemies[int(random.random() * (len(enemies)-1))]))
                    enemy_shots.append(Enemy_shot(enemy_shot_img, enemies[random.randint(0, len(enemies)-1)]))
            #i = i + 1

            for y in enemy_shots:
                if y.collision_check(player):
                    enemy_shots.remove(y)
                    player.health -= 1
                    if player.health == 0:
                        health.image = health_img_0
                        player.alive = False
                        self.gameover = True
                    elif player.health == 1:
                        hit_audio.play()
                        health.image = health_img_1
                    elif player.health == 2:
                        hit_audio.play()
                        health.image = health_img_2

            # Check for collisions
            for enemy in enemies:
                if enemy.collision_check(player):
                    enemies.remove(enemy)
                    player.health -= 1
                    if player.health == 0:
                        health.image = health_img_0
                        player.alive = False
                        self.gameover = True
                    elif player.health == 1:
                        hit_audio.play()
                        health.image = health_img_1
                    elif player.health == 2:
                        hit_audio.play()
                        health.image = health_img_2

                #enemies go away once they hit the bottom
                if enemy.rect.y >= const.SCREENRECT.height - 30:
                    enemies.remove(enemy)


                for shot in shots:
                    if shot.collision_check(enemy):
                        enemy_audio.play()
                        shots.remove(shot)
                        enemies.remove(enemy)
                        self.score += 1

            # Draw actors
            for actor in [player] + [health] + enemies + shots + enemy_shots + recover_health:
                render = actor.draw(self.screen)
                actors.append(render)

            # Update actors
            pygame.display.update(actors)
            actors = []

        # Exit game and system
        if self.gameover:
            gameover_audio.play()
        pygame.time.delay(2000)
        pygame.display.quit()
        pygame.quit()
        sys.exit()
