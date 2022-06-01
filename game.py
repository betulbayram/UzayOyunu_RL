from enum import Enum #enumarate etmek
import pygame 
import random
import math
import numpy as np

# initializing pygame
pygame.init()


#aksiyonlar numaralandirildi
class Actions(Enum):
    LEFT = 0
    RIGHT = 1
    SHOOT = 2



class SpaceInvaders:
    
    """
        Uzay Oyunu, 2 boyutlu score sayisina bağli bir strateji oyunudur.
        Oyun bileşenleri canavarlar, uzay gemisi ve mermiden oluşmaktadir.
        Random şekilde üretilen canavarlari uzay gemisinin collision alanina 
        gelmeden belli bir rest süresiyle vurmaya çalişan bir uzay gemisinden oluşmaktadir.
        Score, vurulan canavar sayisina göre artmaktadir.
        Vurulan canavar ekrandan kaybolmaktadir.
    """


    def __init__(self):
        self.screen_width = 800 #frame genişliği
        self.screen_height = 600 #frame yüksekliği 
        self.score_val = 0 #vurulan canavar sayisina bagli olarak artan score sayisi
        self.scoreX = 1 #score sayacının genisligi
        self.scoreY = 5 #score saycinin yuksekligi
        self.font = pygame.font.Font('freesansbold.ttf', 20) #yazi fontu ve boyutu
        self.playerImage = pygame.image.load('data\\spaceship.png') #oyuncunun fotografi yuklenir
        self.player_X = 370 #oyuncunun baslangictaki x degeri
        self.player_Y = 523 #oyuncunun baslangictak y degeri
        self.player_Xchange = 0 #oyuncunun baslangicta x eksenindeki hareketi
        self.bulletImage = pygame.image.load('data\\bullet.png') #merminin fotografi yuklenir
        self.bullet_X = 0 #merminin baslangictaki x konumu
        self.bullet_Y = 500 #merminin baslangictaki y konumu
        self.bullet_Xchange = 0 #merminin baslangicta x eksenindeki hareketi
        self.bullet_Ychange = 2 #merminin baslangicta y eksenindeki hareketi
        self.bullet_state = "rest" #merminin baslangictaki rest durumu
        self.alienImage = [] #spawn olan uzayliların fotograf listesi
        self.alien_X = [] #spawn olan uzayliların x konumlari listesi
        self.alien_Y = [] #spawn olan uzaylilarin y konumlari listesi
        self.closest_alien_x = 0 #en yakin uzayliyi baslangicta 0 olarak kabul eder
        self.alien_Xchange = [] #uzaylilarin x eksenindeki hareket listesi
        self.alien_Ychange = [] #uzaylilarin y eksenindeki hareket listesi
        self.no_of_aliens = 15 #spawn olacak uzaylilarin sayisi
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height)) #frame görsellestirilmesi
        pygame.display.set_caption("Yapay Zeka ile Uzay Oyunu") #frame basligi
        self.reset() #oyunun resetlenmesi

    def show_score(self,x, y):
        """
            x: self.scoreX
            y: self.scoreY

            Scoreu surekli x, y konumlarinda gosteren fonksiyon.
        """
        score = self.font.render("Points: " + str(self.score_val), True, (255,255,255)) #scoreu tanimlar boolean olan değer yazinin yumuşakliği sondaki ise renktir
        self.screen.blit(score, (x , y ))


    def create_inv(self):
        for num in range(self.no_of_aliens):
            self.alienImage.append(pygame.image.load('data\\alien.png'))
            self.alien_X.append(random.randint(64, 737))
            self.alien_Y.append(random.randint(30, 180))
            self.alien_Xchange.append(0.8)
            self.alien_Ychange.append(100)

    def destroy_aliens(self):
         self.alien_X.clear()
         self.alien_Y.clear()

    def find_closest(self):
        self.closest_alien_x = self.alien_X[0]
        for d in range(len(self.alien_X)):
            if self.alien_X[d] < self.closest_alien_x:
                self.closest_alien_x = self.alien_X[d]


    def reset(self):
        self.direction = Actions.RIGHT
        self.player_X = 370
        self.player_Y = 523
        self.score_val = 0
        self.destroy_aliens()
        self.create_inv()   


    def isCollision(self, x1, x2, y1, y2): #çarpiiacak cisimlerin korrdinatlari
        distance = math.sqrt((math.pow(x1 - x2,2)) + (math.pow(y1 - y2,2))) #çarpiiacak cisimlerin arasi uzaklik
        if distance <= 50:
            return True #çarpişti
        else:
            return False

    def player(self, x, y):
        self.screen.blit(self.playerImage, (x - 16, y + 10)) #playerin x ve y sini değiştiriyor

    def alien(self, x, y, i):
        self.screen.blit(self.alienImage[i], (x, y)) #blit fonk verilen koordinatlarda verilen resmi ekrana getirir

    def bullet(self, x, y):
        self.screen.blit(self.bulletImage, (x, y))
        self.bullet_state = "fire"

    def move(self, action):
        self.find_closest()
        clock_wise = [Actions.LEFT, Actions.RIGHT, Actions.SHOOT]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 3
            new_dir = clock_wise[next_idx]
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 3
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        if self.direction == Actions.LEFT:
            self.player_Xchange = -1.0
        elif self.direction == Actions.RIGHT:
            self.player_Xchange = 1.0
        elif self.direction == Actions.SHOOT:
            if self.bullet_state is "rest":
                self.bullet_X = self.player_X
                self.bullet(self.bullet_X, self.bullet_Y)         

    def play_step(self, action):

        self.screen.fill((0, 0, 0))

    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        self.move(action)

        reward = 0
        game_over = False

        self.player_X += self.player_Xchange
        for i in range(self.no_of_aliens):
            self.alien_X[i] += self.alien_Xchange[i]


        if self.bullet_Y <= 0:
            self.bullet_Y = 600
            self.bullet_state = "rest"
        if self.bullet_state is "fire":
            self.bullet(self.bullet_X, self.bullet_Y)
            self.bullet_Y -= self.bullet_Ychange

        for i in range(self.no_of_aliens):
            
            if self.alien_Y[i] >= 450:
                if abs(self.player_X-self.alien_X[i]) < 80:
                    for j in range(self.no_of_aliens):
                        self.alien_Y[j] = 2000
                    game_over = True
                    reward = -10
                return reward, game_over, self.score_val

            if self.alien_X[i] >= 735 or self.alien_X[i] <= 0:
                self.alien_Xchange[i] *= -1
                self.alien_Y[i] += self.alien_Ychange[i]

            collision = self.isCollision(self.bullet_X, self.alien_X[i], self.bullet_Y, self.alien_Y[i])
            if collision:
                reward  = 10
                self.score_val += 1
                self.bullet_Y = 600
                self.bullet_state = "rest"
                self.alien_X[i] = random.randint(64, 736)
                self.alien_Y[i] = random.randint(30, 200)
                self.alien_Xchange[i] *= -1
            
            self.alien(self.alien_X[i], self.alien_Y[i], i)

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