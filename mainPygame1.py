import random
import pygame

from pygame.locals import *
from config import *
from elements import *
from planets import *

images = {
    "Ouest": {"Joueur": []},
    "Est": {"Joueur": []}
}

sheet_Joueur = pygame.image.load("pré_rapport/Images/Joueur.png")
height = sheet_Joueur.get_height()
width = sheet_Joueur.get_width() // 3

for i in range(3):
    image = sheet_Joueur.subsurface([width * i, 0, width, height])
    images["Ouest"]["Joueur"].append(image)
    images["Est"]["Joueur"].append(pygame.transform.flip(image, True, False))

for j in images.keys():
    for i in range(len(images[j]["Joueur"])):
        images[j]["Joueur"][i] = pygame.transform.scale(images[j]["Joueur"][i], (50, 80))

class JoueurPygame(pygame.sprite.Sprite):

    is_created = False
    
    def __init__(self,all_sprites):
        pygame.sprite.Sprite.__init__(self)
        self.all_sprites = all_sprites
        self.num_image = 0
        self.direction_x = "Ouest"
        self.direction_y = "Sud"
        self.cpt = 0
        self.dx = -1
        self.dy = 1
        self.image = images[self.direction_x]["Joueur"][self.num_image]
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 200
        self.speed_x = 1.55
        self.speed_y = 1.55
        self.timer = pygame.time.get_ticks()
        self.is_moving = False
        self.health = 30
        self.derniere_col = 0

    def attack(self, other_sprite):
        current_time = pygame.time.get_ticks()
        time_since_col = current_time - self.derniere_col
        if time_since_col < 10000:
            return
        if isinstance(other_sprite,self.__class__) and not self.is_created:
            new_sprite = self.__class__(self.all_sprites)
            self.rect.x -= 40
            other_sprite.rect.x += 40
            new_sprite.rect.x = (self.rect.x + other_sprite.rect.x)// 2
            new_sprite.rect.y = (self.rect.y + other_sprite.rect.y) // 2
            new_sprite.is_created = True
            self.all_sprites.add(new_sprite)
            self.is_created = True
        elif not isinstance(other_sprite,self.__class__):
            other_sprite.health -= 30
            if other_sprite.health <= 0:
                other_sprite.kill()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed_x
            self.direction_x = "Ouest"
            self.is_moving = True
        elif keys[K_RIGHT]:
            self.rect.x += self.speed_x
            self.direction_x = "Est"
            self.is_moving = True
        elif keys[K_UP]:
            self.rect.y -= self.speed_y
            self.is_moving = True
        elif keys[K_DOWN]:
            self.rect.y += self.speed_y
            self.is_moving = True
        else:
            self.is_moving = False
        if keys[K_LEFT] and keys[K_UP]:
            self.rect.x -= self.speed_x - 1
            self.rect.y -= self.speed_y - 1
            self.direction_x = "Ouest"
            self.direction_y = "Nord"
        elif keys[K_LEFT] and keys[K_DOWN]:
            self.rect.x -= self.speed_x - 1
            self.rect.y += self.speed_y - 1
            self.direction_x = "Ouest"
            self.direction_y = "Sud"
        elif keys[K_RIGHT] and keys[K_UP]:
            self.rect.x += self.speed_x - 1
            self.rect.y -= self.speed_y - 1
            self.direction_x = "Est"
            self.direction_y = "Nord"
        elif keys[K_RIGHT] and keys[K_DOWN]:
            self.rect.x += self.speed_x - 1
            self.rect.y += self.speed_y - 1
            self.direction_x = "Est"
            self.direction_y = "Sud"

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > width - self.rect.width:
            self.rect.x = width - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > height - self.rect.height:
            self.rect.y = height - self.rect.height
        if self.direction_x == "Ouest":
            self.image = images["Ouest"]["Joueur"][self.num_image]
        elif self.direction_x == "Est":
            self.image = images["Est"]["Joueur"][self.num_image]

        if self.is_moving:
            self.cpt += 1
            if self.cpt == 10:
                self.cpt = 0
                self.num_image += 1
                if self.num_image == len(images[self.direction_x]["Joueur"]):
                    self.num_image = 0
            self.image = images[self.direction_x]["Joueur"][self.num_image]
        else:
            self.image = images[self.direction_x]["Joueur"][0]

        collided_walls = pygame.sprite.spritecollide(self, walls, False)
        if collided_walls:
            self.rect.x -= self.dx * self.speed_x
            self.rect.y -= self.dy * self.speed_y
            self.dx = -self.dx
            self.dy = -self.dy

        colliding_sprites = pygame.sprite.spritecollide(self,self.all_sprites,False)
        for sprite in colliding_sprites:
            if sprite != self :
                self.attack(sprite)



if __name__ == "__main__":
    pygame.init()

    width = 1000
    height = 750

    screen = pygame.display.set_mode((width,height))
    background = pygame.image.load("pré_rapport/Images/map.png")
    background = pygame.transform.scale(background,(width,height))

    running = True
    all_sprites = pygame.sprite.Group()

    char1 = HumainPygame(all_sprites)
    char2 = ChevalierPygame(all_sprites)
    char3 = VachePygame(all_sprites)
    char4 = DragonPygame(all_sprites)
    char5 = LapinPygame(all_sprites)
    char6 = LionPygame(all_sprites)
    char7 = SerpentPygame(all_sprites)
    char8 = SourisPygame(all_sprites)
    char9 = OeufPygame(all_sprites)
    char10 = OeufSerpentPygame(all_sprites)
    char11 = JoueurPygame(all_sprites)
    char12 = HumainPygame(all_sprites)
    char13 = VachePygame(all_sprites)
    char14 = ChevalierPygame(all_sprites)
    char15 = LapinPygame(all_sprites)
    char16 = LionPygame(all_sprites)
    char17 = SerpentPygame(all_sprites)
    char18 = SourisPygame(all_sprites)

    all_sprites.add(char1)
    all_sprites.add(char2)
    all_sprites.add(char3)
    all_sprites.add(char4)
    all_sprites.add(char5)
    all_sprites.add(char6)
    all_sprites.add(char7)
    all_sprites.add(char8)
    all_sprites.add(char9)
    all_sprites.add(char10)
    all_sprites.add(char11)
    all_sprites.add(char12)
    all_sprites.add(char13)
    all_sprites.add(char14)
    all_sprites.add(char15)
    all_sprites.add(char16)
    all_sprites.add(char17)
    all_sprites.add(char18)

    char12.rect.x = 460
    char12.rect.y = 450
    char13.rect.x = 600
    char13.rect.y = 350
    char14.rect.x = 150
    char14.rect.y = 350
    char15.rect.x = 220
    char15.rect.y = 490
    char16.rect.x = 700
    char16.rect.y = 460
    char17.rect.x = 370
    char17.rect.y = 60
    char18.rect.x = 50
    char18.rect.y = 200

    while running:
        screen.blit(background,(0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()
    pygame.quit()

