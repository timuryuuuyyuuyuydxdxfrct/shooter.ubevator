from pygame import *
from random import randint
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg') 
lose = 0
score = 0
max_lose = 10
max_score = 300
font.init()
font1 = font.SysFont('Arial',36)
font2 = font.SysFont('Arial',80)
win = font2.render('doctorochko', True, (43, 42, 123))
lost = font2.render('obamayobanikozel', True, (221, 221, 221))
life = 5

class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 10:
            self.rect.x -= self.speed
        if keys [K_d] and self.rect.x < width - 80:
            self.rect.x += self.speed
    def attack(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 100)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lose 
        if self.rect.y > height:
            self.rect.x = randint(80,width-80)
            self.rect.y = 0
            lose += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

        pass
width = 700
height = 500
asteroids = sprite.Group()
for i in range(1,6):
    asteroid = Enemy('asteroid.png', randint(80,width-80), -40, randint(1,15))    
    asteroids.add(asteroid)
window = display.set_mode((width, height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(width, height))
hero = Player('rocket.png', 350, height - 100, 20)
monsters = sprite.Group()
for i in range(1,8):
    enemy = Enemy('ufo.png', randint(80,width-80),-50,randint(1,7))
    monsters.add(enemy)
bullets = sprite.Group()
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                hero.attack()
    
    
    if not finish:
        window.blit(background, (0,0))
        text_lose = font1.render('Попущено:'+str(lose), True, (234, 243, 99))
        text_win = font1.render('Принц Уэльский:' +str(score), True, (213, 54, 213))
        hero.reset()
        hero.update()
        window.blit(text_win, (10,20))
        window.blit(text_lose, (500,20))
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        collides1 = sprite.groupcollide(asteroids, bullets, True, True)
        for c in collides:
            score += 1
            enemy = Enemy('ufo.png', randint(80, width-80), -40, randint(1,7))
            monsters.add(enemy)
        if sprite.spritecollide(hero, monsters, False) or sprite.spritecollide(hero,asteroids,False):
            sprite.spritecollide(hero,monsters,True)
            sprite.spritecollide(hero,asteroids,True)
            life -= 1
        if life == 0 or lose>max_lose:
            finish = True
            window.blit(lost,(300,250))
        if score >= max_score:
            finish = True
            window.blit(win, (300,250))
        if life > 3:
            life_color = (0,250,0)
        if life >= 2 and life <= 3:
            life_color = (125,55,0)
        text_life = font1.render(str(life),True, life_color)
        window.blit(text_life, (350,0))
        display.update()
    else:
        finish = False
        score = 0
        lose = 0
        life = 5
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time_delay(3000)
        for i in range(1,8):
            enemy = Enemy('ufo.png', randint(80,width-80),-50,randint(1,7))
            monsters.add(enemy)
        for i in range(1,6):
            asteroid = Enemy('asteroid.png', randint(80,width-80), -40, randint(1,15))    
            asteroids.add(asteroid)
    time.delay(50)
