import pygame
import random

pygame.init()

win = pygame.display.set_mode((750, 750))

pygame.display.set_caption('Space Invaders')

bg = pygame.image.load('background.png')

white = (255, 255, 255)

green = (0, 255, 0)

red = (255, 0 , 0)

black = (0, 0 , 0)

blue = (83, 135, 209)

purple = (102, 0, 102)

lightpurple = (153, 0, 153)

gray = (128, 128, 128)

class Ship(pygame.sprite.Sprite):
    def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('ship.png')
            self.rect = self.image.get_rect()
            self.lives = 5
            self.score = 0
            self.level = 1
            self.highscore = 0
    
    def draw(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy.png')
        self.rect = self.image.get_rect()
        self.group_rect = pygame.Rect(130, 75, 500, 250)
        self.direction = ship.level * 2
        self.lives = ship.level 

    def update(self):
        self.rect.x += self.direction
        self.group_rect.x += self.direction
        if self.group_rect.x + 500 >= 725:
            self.direction = -self.direction
        if self.group_rect.x <= 25:
            self.direction = -self.direction
            self.rect.y += 5

class Bunker(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bunker.png')
        self.rect = self.image.get_rect()

class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ammunition.png')
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += -10

class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bomb.png')
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 10

ship = Ship()
ship.rect.x = 335
ship.rect.y = 650

enemy_list = pygame.sprite.Group()
bunker_list  = pygame.sprite.Group()
missile_list = pygame.sprite.Group()
bomb_list = pygame.sprite.Group()


def make_enemies():

    for row in range(1, 6):
        for column in range(1, 11):
            enemy = Enemy()
            enemy.rect.x = 80 + (50 * column)
            enemy.rect.y = 25 + (50 * row)
            enemy_list.add(enemy)

make_enemies()

#Cretae bunkers
def make_bunkers():
    for bunk in range(3):
        for row in range(5):
            for column in range(10):
                bunker = Bunker()
                bunker.rect.x = (50 + (275 * bunk)) + (10 * column)
                bunker.rect.y = 500 + (10 * row)
                bunker_list.add(bunker)

make_bunkers()

def redraw():
    win.blit(bg, (0, 0))
    if playing:
        bottom = pygame.draw.rect(win, white, (50, 700, 650, 5))
        
        #Ship lives
        for i in range(ship.lives):
            pygame.draw.rect(win, red, (50 + (i* 130), 715, 130, 15))
        
        #Game Title
        font = pygame.font.SysFont('Courier New', 30)
        text = font.render('Space Invaders', False, white)
        textRect = text.get_rect()
        textRect.center = (750//2, 25)
        win.blit(text, textRect)

        #Level
        text = font.render('Level:' + str(ship.level), False, white)
        textRect = text.get_rect()
        textRect.center = (100, 25)
        win.blit(text, textRect)

        #Score
        text = font.render('Score:' + str(ship.score), False, white)
        textRect = text.get_rect()
        textRect.center = (650, 25)
        win.blit(text, textRect)
        
        #Draw Objects
        ship.draw()
        enemy_list.update()
        enemy_list.draw(win)
        bunker_list.draw(win)
        missile_list.update()
        missile_list.draw(win)
        bomb_list.update()
        bomb_list.draw(win)
    else:
        #Title
        font = pygame.font.SysFont('Courier New', 60)
        text = font.render('Space Invaders', False, green)
        textRect = text.get_rect()
        textRect.center = (750//2, 50)
        win.blit(text, textRect)

        #Highscore
        font = pygame.font.SysFont('Courier New', 40)
        text = font.render('Highscore:' + str(ship.highscore), False, white)
        textRect = text.get_rect()
        textRect.center = (750//2, 750//2)
        win.blit(text, textRect)

        #Start Message
        font = pygame.font.SysFont('Courier New', 50)
        text = font.render('Press Space To Start', False, white)
        textRect = text.get_rect()
        textRect.center = (750//2, 700)
        win.blit(text, textRect)


    #Update display
    pygame.display.update()

run = True

playing = False

while run:

    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    if playing:
    #Movement controls
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            ship.rect.x += -10
        if key[pygame.K_RIGHT]:
            ship.rect.x += 10
        if key[pygame.K_SPACE]:
            if len(missile_list) < 20:
                missile = Missile()
                missile.rect.x = ship.rect.x + 40
                missile.rect.y = ship.rect.y
                missile_list.add(missile)

        shoot_chance = random.randint(1, 100)
        bomb_chance = ship.level * 5

        if shoot_chance < bomb_chance:
            if len(enemy_list) > 0:
                random_enemy = random.choice(enemy_list.sprites())
                bomb = Bomb()
                bomb.rect.x = random_enemy.rect.x + 12
                bomb.rect.y = random_enemy.rect.y + 25

                bomb_list.add(bomb)
        
        for missile in missile_list:
            if missile.rect.y < -10:
                missile_list.remove(missile)

            for enemy in enemy_list:
                if missile.rect.colliderect(enemy.rect):
                    ship.score += 1
                    missile_list.remove(missile)
                    enemy.lives -= 1
                    if enemy.lives <= 0:
                        enemy_list.remove(enemy)

            for bunker in bunker_list:
                if missile.rect.colliderect(bunker.rect):
                    missile_list.remove(missile)
                    bunker_list.remove(bunker)
        
        for bomb in bomb_list:
            if bomb.rect.y > 750:
                bomb_list.remove(bomb)
            if bomb.rect.colliderect(ship.rect):
                bomb_list.remove(bomb)
                ship.lives -= 1
            for bunker in bunker_list:
                if bomb.rect.colliderect(bunker.rect):
                    bomb_list.remove(bomb)
                    bunker_list.remove(bunker)
        
        if ship.lives < 0:
            
            playing = False

            if ship.score > ship.highscore:
                ship.highscore = ship.score
            
            ship.lives = 5
            enemy.lives = 1
        
        if len(enemy_list) == 0:
            make_enemies()
            ship.level += 1
    
    else:
        bomb_list.empty()
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            playing = True
            ship.level = 1
            ship.score = 0
        
            bunker_list.empty()
            make_bunkers()

            enemy_list.empty()
            make_enemies()


    redraw()
    
pygame.quit()