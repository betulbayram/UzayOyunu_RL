from enum import Enum
import pygame
import random
import math
from pygame import mixer
import numpy as np
# initializing pygame
pygame.init()


class Actions(Enum):
    LEFT = 0
    RIGHT = 1
    SHOOT = 2

class SpaceInvaders:

    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.score_val = 0
        self.scoreX = 5
        self.scoreY = 5
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.playerImage = pygame.image.load('data\\spaceship.png')
        self.player_X = 370
        self.player_Y = 523
        self.player_Xchange = 0
        self.bulletImage = pygame.image.load('data\\bullet.png')
        self.bullet_X = 0
        self.bullet_Y = 500
        self.bullet_Xchange = 0
        self.bullet_Ychange = 2
        self.bullet_state = "rest"
        self.invaderImage = []
        self.invader_X = []
        self.invader_Y = []
        self.closest_invader_x = 0
        self.invader_Xchange = []
        self.invader_Ychange = []
        self.no_of_invaders = 15
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Yapay Zeka ile Uzay Oyunu")
        self.game_over_font = pygame.font.Font('freesansbold.ttf', 64)
        self.reset()

    def show_score(self,x, y):
        score = self.font.render("Points: " + str(self.score_val), True, (255,255,255))
        self.screen.blit(score, (x , y ))


    def create_inv(self):
        for num in range(self.no_of_invaders):
            self.invaderImage.append(pygame.image.load('data\\alien.png'))
            self.invader_X.append(random.randint(64, 737))
            self.invader_Y.append(random.randint(30, 180))
            self.invader_Xchange.append(0.8)
            self.invader_Ychange.append(100)

    def destroy_invaders(self):
         self.invader_X.clear()
         self.invader_Y.clear()

    def find_closest(self):
        self.closest_invader_x = self.invader_X[0]
        for d in range(len(self.invader_X)):
            if self.invader_X[d] < self.closest_invader_x:
                self.closest_invader_x = self.invader_X[d]


    def reset(self):
        # init game state
        self.direction = Actions.RIGHT
        self.player_X = 370
        self.player_Y = 523
        self.score_val = 0
        self.destroy_invaders()
        self.create_inv()   


    def isCollision(self, x1, x2, y1, y2):
        distance = math.sqrt((math.pow(x1 - x2,2)) + (math.pow(y1 - y2,2)))
        if distance <= 50:
            return True
        else:
            return False

    def player(self, x, y):
        self.screen.blit(self.playerImage, (x - 16, y + 10))

    def invader(self, x, y, i):
        self.screen.blit(self.invaderImage[i], (x, y))

    def bullet(self, x, y):
        self.screen.blit(self.bulletImage, (x, y))
        self.bullet_state = "fire"

    def move(self, action):
        #left, right, shoot
        self.find_closest()
        clock_wise = [Actions.LEFT, Actions.RIGHT, Actions.SHOOT]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 3
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 3
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        if self.direction == Actions.LEFT:
            self.player_Xchange = -1.0
        elif self.direction == Actions.RIGHT:
            self.player_Xchange = 1.0
        elif self.direction == Actions.SHOOT:
            if self.bullet_state is "rest":
                self.bullet_X = self.player_X
                self.bullet(self.bullet_X, self.bullet_Y)         


    # game loop
    def play_step(self, action):

        self.screen.fill((0, 0, 0))

    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        self.move(action)

        reward = 0
        game_over = False

        # adding the change in the player position
        self.player_X += self.player_Xchange
        for i in range(self.no_of_invaders):
            self.invader_X[i] += self.invader_Xchange[i]

        # bullet movement
        if self.bullet_Y <= 0:
            self.bullet_Y = 600
            self.bullet_state = "rest"
        if self.bullet_state is "fire":
            self.bullet(self.bullet_X, self.bullet_Y)
            self.bullet_Y -= self.bullet_Ychange

        # movement of the invader
        for i in range(self.no_of_invaders):
            
            if self.invader_Y[i] >= 450:
                if abs(self.player_X-self.invader_X[i]) < 80:
                    for j in range(self.no_of_invaders):
                        self.invader_Y[j] = 2000
                    game_over = True
                    reward = -10
                return reward, game_over, self.score_val

            if self.invader_X[i] >= 735 or self.invader_X[i] <= 0:
                self.invader_Xchange[i] *= -1
                self.invader_Y[i] += self.invader_Ychange[i]

            # Collision
            collision = self.isCollision(self.bullet_X, self.invader_X[i], self.bullet_Y, self.invader_Y[i])
            if collision:
                reward  = 10
                self.score_val += 1
                self.bullet_Y = 600
                self.bullet_state = "rest"
                self.invader_X[i] = random.randint(64, 736)
                self.invader_Y[i] = random.randint(30, 200)
                self.invader_Xchange[i] *= -1
            
            self.invader(self.invader_X[i], self.invader_Y[i], i)

        if self.player_X <= 16:
            self.player_X = 16
        elif self.player_X >= 750:
            self.player_X = 750

        self.player(self.player_X, self.player_Y)
        self.show_score(self.scoreX, self.scoreY)
        pygame.display.update()

        return reward, game_over, self.score_val

if __name__ == '__main__':
    g = SpaceInvaders().play_step()