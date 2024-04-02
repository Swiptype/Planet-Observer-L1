import random
import pygame
import time

class Element:
    ids_count = 0
    
    def __init__(self, name, char_repr):
        self.__name = name
        self.__id = self.ids_count
        self.__char_repr = char_repr
        Element.ids_count += 1

    def get_name(self):
        return self.__name

    def get_id(self):
        return self.__id

    def get_char_repr(self):
        return self.__char_repr

    def __repr__(self):
        return f"{self.__char_repr} : {self.__name} {self.get_id()}"

    def __eq__(self, other):
        return type(self) is type(other)

    def __ne__(self, other):
        return not self.__eq__(other)

class Animal(Element):
    age = 0
    bar_life = [0,0]
    current_direction = [0,0]
    race = ''
    evenements = ["Tornade","Seisme","Tsunami","Eruption volcanique","Meteorites","Manifestation d'animaux"]

    def __init__(self,name,char_repr,life_max,race,degats):
        super().__init__(name, char_repr)
        self.life_max = life_max
        self.life = life_max
        Animal.bar_life[0] = self.life
        Animal.bar_life[1] = life_max
        self.gender = random.randint(0, 1)
        self.race = race
        self.degats = degats
        self.derniere_apparition = 0

    def get_age(self):
        return f"{self.get_gender()} de {self.age} an(s)"

    def ageing(self):
        Animal.age += 1

    def get_gender(self):
        if self.gender == 0:
            return f'Femelle'
        if self.gender == 1:
            return f'Male'

    def get_life_max(self):
        return self.life_max

    def get_life(self):
        return self.life

    def is_alive(self):
        return self.get_life() > 0

    def is_dead(self):
        return not self.is_alive()

    def recovering_life(self, value):
        #self.bar_life[0] = min(self.bar_life[0] + value, self.bar_life[1])
        Animal.bar_life[0] += value

    def losing_life(self, value):
        #self.bar_life[0] = max(self.bar_life[0] - value, 0)
        Animal.bar_life[0] -= value

    def get_current_direction(self):
        return Animal.current_direction

    def set_current_direction(self,line_direction,column_direction):
        Animal.current_direction = [line_direction,column_direction]

    def __repr__(self):
        return f"{self.get_char_repr()} : {self.get_name()} ID {self.get_id()} {self.get_age()}\n - Barre de vie : {self.bar_life}"

    def attack(self, other):
        other.life -= self.degats
        if other.life < 0:
            other.life = 0
        Animal.bar_life[0] = other.life

    def apparition_animal(self, autre_animal):
        current_time = time.time()
        if self.race == autre_animal.race and self.collide_with(autre_animal):
            if current_time - self.derniere_apparition > 10:
                plus_animal = type(self)()
                return plus_animal
        else:
            raise ValueError("Les deux animaux ne peuvent pas se reproduire.")

    def sauvetage(self):
        value = random.randint(0,1)
        if value == 1:
            i = random.randint(0, len(Animal.evenements)-1)
            print(self.get_name(), "s'est échappé grâce à", Animal.evenements[i])
            return False;
        else:
            print(self.get_name(), "ne peut pas s'échapper")
            return True;

    def duel(self, other):
        if self.sauvetage() == False:
            pass
        else:
            print("Le duel entre", self.get_name()," et ",other.get_name()," commence !")
            while self.life > 0 and other.life > 0:
                self.attack(other)
                if other.life <= 0:
                    return f"{self.get_name()} a gagné !"
                other.attack(self)
                if self.life <= 0:
                    return f"{other.get_name()} a gagné !"

class Mouse(Animal):
    def __init__(self):
        super().__init__("Mouse","\U0001F42D",2,"Mouse",1)
    
class Lion(Animal):
    def __init__(self):
        super().__init__("Lion","\U0001F981",10,"Lion",7.5)

class Dragon(Animal):
    def __init__(self):
        super().__init__("Dragon","\U0001F432",20,"Dragon",9)

class Cow(Animal):
    def __init__(self):
        super().__init__("Cow","\U0001F42E",5,"Cow",3)

""" Ajout de quelques animaux supplémentaires :"""

class Serpent(Animal):
    def __init__(self):
        super().__init__("Serpent","\U0001F40D",5,"Serpent",2.5)

class Lapin(Animal):
    def __init__(self):
        super().__init__("Lapin","\U0001f430",2.5,"Lapin",0.5)

class Oeuf(Animal):
    def __init__(self):
        super().__init__("Oeuf","\U0001F95A",1,"Oeuf",0)

class OeufSerpent(Animal):
    def __init__(self):
        super().__init__("OeufSerpent","\U0001FABA",1,"OeufSerpent",0)

class Portee(Animal):
    def __init__(self):
        self.portee = random.randint(1, 12)
        super().__init__("Portee", "\U0001F42D", 1, "Lapin", 0)
        self.lapins = []

        def __repr__(self):
            return f"L'accouplement a donné une portée de {self.portee} lapins"

        for i in range(self.portee):
            lapin = Lapin()
            self.lapins.append(lapin)

class Ground(Element) :
    def __init__(self):
        super().__init__("Ground", ".")

    def __repr__(self):
        return f"{self.get_char_repr()} : {self.get_name()} {self.get_id()}"

class Resource(Element) :
    def __init__(self,name,char_repr,value):
        super().__init__(name,char_repr)
        self.__value = value

    def get_value(self):
        return self.__value

    def __repr__(self):
        return f"{self.get_char_repr()} : {self.get_name()} {self.get_id()} ({self.get_value()})"

class Herb(Resource) :
    def __init__(self):
        super().__init__("Herb","\U0001F33F",1)
        self.rect = self.image.get_rect()

class Water(Resource):
    def __init__(self):
        super().__init__("Water","\U0001F41F",2)


""" Ajout d'Humain :"""

class Humain(Element) :
    age = 0
    gender = 0
    bar_life = [0,0]
    current_direction = [0,0]

    def __init__(self,name,char_repr,life_max,race,degats):
        super().__init__(name, char_repr)
        self.life_max = life_max
        self.life = life_max
        Humain.bar_life[0] = self.life
        Humain.bar_life[1] = life_max
        self.gender = random.randint(0, 1)
        self.race = race
        self.degats = degats
        self.derniere_apparition = 0

    def get_age(self):
        return f"{self.get_gender()} de {self.age} an(s)"

    def ageing(self):
        Humain.age += 1

    def get_gender(self):
        if Humain.gender == 0:
            return f'Femelle'
        if Humain.gender == 1:
            return f'Male'

    def get_life_max(self):
        return self.life_max

    def get_life(self):
        return self.life

    def is_alive(self):
        self.get_life() > 0

    def is_dead(self):
        return not self.is_alive()

    def recovering_life(self, value):
        #self.bar_life[0] = min(self.bar_life[0] + value, self.bar_life[1])
        Humain.bar_life[0] += value

    def losing_life(self, value):
        #self.bar_life[0] = max(self.bar_life[0] - value, 0)
        Humain.bar_life[0] -= value

    def get_current_direction(self):
        return Humain.current_direction

    def set_current_direction(self,line_direction,column_direction):
        Humain.current_direction = [line_direction,column_direction]

    def __repr__(self):
        return f"{self.get_char_repr()} : {self.get_name()} ID {self.get_id()} {self.get_age()}\n - Barre de vie : {self.bar_life}"

    def apparition_humain(self,humain):
        current_time = time.time()
        if self.race == "Humain" and humain.race == "Humain" and self.collide_with(humain):
            if current_time - self.derniere_apparition > 30:
                plus_humain = Homme()
                return plus_humain
        else:
            return None

    def attack(self, other):
        other.life -= self.degats
        if other.life < 0:
            other.life = 0
        Animal.bar_life[0] = other.life

    def sauvetage(self):
        value = random.randint(0,1)
        if value == 1:
            i = random.randint(0, len(Animal.evenements)-1)
            print(self.get_name(), "s'est échappé grâce à", Animal.evenements[i])
            return False;
        else:
            print(self.get_name(), "ne peut pas s'échapper")
            return True;

    def duel(self, other):
        if self.sauvetage() == False:
            pass
        else:
            print("Le duel entre", self.get_name()," et ",other.get_name()," commence !")
            while self.life > 0 and other.life > 0:
                self.attack(other)
                if other.life <= 0:
                    return f"{self.get_name()} a gagné !"
                other.attack(self)
                if self.life <= 0:
                    return f"{other.get_name()} a gagné !"


class Chevalier(Humain):
    def __init__(self):
        super().__init__("Chevalier", "\U0001F6E1",15,"Humain",10)

class Homme(Humain):
    def __init__(self):
        super().__init__("Homme", "\U0001F64D",10,"Humain",5)

class Joueur(Humain):
    def __init__(self):
        super().__init__("Joueur","\U0001F451",30,"Humain",10)

HEIGHT = 50
WIDTH = 25

images = {"Est" : {"Humain": [], "Chevalier": [], "Vache":[],"Dragon":[], "Lapin":[],"Lion":[],"Oeuf":[],"OeufSerpent":[],"Serpent":[],"Souris":[],"Joueur":[]}, 
          "Ouest" : {"Humain": [], "Chevalier": [], "Vache": [],"Dragon":[], "Lapin":[],"Lion":[],"Oeuf":[],"OeufSerpent":[],"Serpent":[],"Souris":[],"Joueur":[]}}

class HumainPygame(pygame.sprite.Sprite):

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
        self.image = images[self.direction_x]["Humain"][self.num_image]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 110
        self.speed_x = random.randint(1, 1)
        self.speed_y = random.randint(1, 1)
        self.health = 10
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
            other_sprite.health -= 5
            if other_sprite.health <= 0:
                other_sprite.kill()

    def update(self):
        self.cpt += 1
        self.rect.x += self.dx * self.speed_x

        if self.rect.left < 0:
            self.dx = 1
            self.direction_x = "Est"
        
        if self.rect.right > pygame.display.get_surface().get_width():
            self.dx = -1
            self.direction_x = "Ouest"

        self.rect.y += self.dy * self.speed_y

        if self.rect.top < 0:
            self.dy = 1
            self.direction_y = "Sud"

        if self.rect.bottom > pygame.display.get_surface().get_height():
            self.dy = -1
            self.direction_y = "Nord"

        if self.dx == 1:
            self.direction_x = "Est"
        else:
            self.direction_x = "Ouest"

        if self.dy == 1:
            self.direction_y = "Sud"
        else:
            self.direction_y = "Nord"

        if self.num_image < len(images[self.direction_x]["Humain"]):
            self.image = images[self.direction_x]["Humain"][self.num_image]

        if self.cpt == 8:
            self.num_image = 0 if self.num_image + 1 > 4 else self.num_image + 1
            self.cpt = 0

        if random.random() < 0.01:
            self.dx = random.choice([-1, 1])
            self.dy = random.choice([-1, 1])
            
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
            
sheet_humain = pygame.image.load("pré_rapport/Images/Human.png")
height = sheet_humain.get_height()
width = sheet_humain.get_width() / 3

for i in range(3):
    image = sheet_humain.subsurface([width * i, 0, width, height])
    images["Ouest"]["Humain"].append(image)
    images["Est"]["Humain"].append(pygame.transform.flip(image, True, False))

for j in images.keys():
    for i in range(len(images[j]["Humain"])):
        images[j]["Humain"][i] = pygame.transform.scale(images[j]["Humain"][i], (WIDTH, HEIGHT))


class ChevalierPygame(pygame.sprite.Sprite):

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
        self.image = images[self.direction_x]["Chevalier"][self.num_image]
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 100
        self.speed_x = random.randint(1, 1)
        self.speed_y = random.randint(1, 1)
        self.health = 15
        self.derniere_col = 0

    def attack(self,other_sprite):
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
            other_sprite.health -= 10
            if other_sprite.health <= 0:
                other_sprite.kill()

    def update(self):
        self.cpt += 1
        self.rect.x += self.dx * self.speed_x

        if self.rect.left < 0:
            self.dx = 1
            self.direction_x = "Est"
        
        if self.rect.right > pygame.display.get_surface().get_width():
            self.dx = -1
            self.direction_x = "Ouest"

        self.rect.y += self.dy * self.speed_y

        if self.rect.top < 0:
            self.dy = 1
            self.direction_y = "Sud"

        if self.rect.bottom > pygame.display.get_surface().get_height():
            self.dy = -1
            self.direction_y = "Nord"

        if self.dx == 1:
            self.direction_x = "Est"
        else:
            self.direction_x = "Ouest"

        if self.dy == 1:
            self.direction_y = "Sud"
        else:
            self.direction_y = "Nord"

        if self.num_image < len(images[self.direction_x]["Chevalier"]):
            self.image = images[self.direction_x]["Chevalier"][self.num_image]

        if self.cpt == 8:
            self.num_image = 0 if self.num_image + 1 > 4 else self.num_image + 1
            self.cpt = 0

        if random.random() < 0.01:
            self.dx = random.choice([-1, 1])
            self.dy = random.choice([-1, 1])
            
        collided_walls = pygame.sprite.spritecollide(self, walls, False)
        if collided_walls:
            self.rect.x -= self.dx * self.speed_x
            self.rect.y -= self.dy * self.speed_y
            self.dx = -self.dx
            self.dy = -self.dy

        collided_lacs = pygame.sprite.spritecollide(self, lac, False)
        if collided_lacs:
            self.rect.x -= self.dx * self.speed_x
            self.rect.y -= self.dy * self.speed_y
            self.dx = -self.dx
            self.dy = -self.dy

        colliding_sprites = pygame.sprite.spritecollide(self,self.all_sprites,False)
        for sprite in colliding_sprites:
            if sprite != self:
                self.attack(sprite)

sheet_chevalier = pygame.image.load("pré_rapport/Images/Chevalier.png")
height = sheet_chevalier.get_height()
width = sheet_chevalier.get_width() / 3

for i in range(3):
    image = sheet_chevalier.subsurface([width * i, 0, width, height])
    images["Ouest"]["Chevalier"].append(image)
    images["Est"]["Chevalier"].append(pygame.transform.flip(image, True, False))

for j in images.keys():
    for i in range(len(images[j]["Chevalier"])):
        images[j]["Chevalier"][i] = pygame.transform.scale(images[j]["Chevalier"][i], (WIDTH, HEIGHT))

class VachePygame(pygame.sprite.Sprite):

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
        self.image = images[self.direction_x]["Vache"][self.num_image]
        self.rect = self.image.get_rect()
        self.rect.x = 325
        self.rect.y = 500
        self.speed_x = random.randint(1, 1)
        self.speed_y = random.randint(1, 1)
        self.health = 5
        self.derniere_col = 0

    def attack(self,other_sprite):
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
            other_sprite.health -=3
            if other_sprite.health <= 0:
                other_sprite.kill()

    def update(self):
        self.cpt += 1
        self.rect.x += self.dx * self.speed_x

        if self.rect.left < 0:
            self.dx = 1
            self.direction_x = "Est"
        
        if self.rect.right > pygame.display.get_surface().get_width():
            self.dx = -1
            self.direction_x = "Ouest"

        self.rect.y += self.dy * self.speed_y

        if self.rect.top < 0:
            self.dy = 1
            self.direction_y = "Sud"

        if self.rect.bottom > pygame.display.get_surface().get_height():
            self.dy = -1
            self.direction_y = "Nord"

        if self.dx == 1:
            self.direction_x = "Est"
        else:
            self.direction_x = "Ouest"

        if self.dy == 1:
            self.direction_y = "Sud"
        else:
            self.direction_y = "Nord"

        if self.num_image < len(images[self.direction_x]["Vache"]):
            self.image = images[self.direction_x]["Vache"][self.num_image]

        if self.cpt == 100:
            self.num_image = 0 if self.num_image + 1 > 1 else self.num_image + 1
            self.cpt = 0

        if random.random() < 0.01:
            self.dx = random.choice([-1, 1])
            self.dy = random.choice([-1, 1])
         
        collided_walls = pygame.sprite.spritecollide(self, walls, False)
        if collided_walls:
            self.rect.x -= self.dx * self.speed_x
            self.rect.y -= self.dy * self.speed_y
            self.dx = -self.dx
            self.dy = -self.dy

        collided_lacs = pygame.sprite.spritecollide(self, lac, False)
        if collided_lacs:
            self.rect.x -= self.dx * self.speed_x
            self.rect.y -= self.dy * self.speed_y
            self.dx = -self.dx
            self.dy = -self.dy

        colliding_sprites = pygame.sprite.spritecollide(self,self.all_sprites,False)
        for sprite in colliding_sprites:
            if sprite != self:
                self.attack(sprite)

sheet_vache = pygame.image.load("pré_rapport/Images/Vache.png")
height = sheet_vache.get_height()
width = sheet_vache.get_width() / 3

for i in range(3):
    image = sheet_vache.subsurface([width * i, 0, width, height])
    images["Ouest"]["Vache"].append(image)
    images["Est"]["Vache"].append(pygame.transform.flip(image, True, False))

for j in images.keys():
    for i in range(len(images[j]["Vache"])):
        images[j]["Vache"][i] = pygame.transform.scale(images[j]["Vache"][i], (50, 100))

class DragonPygame(pygame.sprite.Sprite):

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
        self.image = images[self.direction_x]["Dragon"][self.num_image]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 600)
        self.rect.y = random.randint(0, 600)
        self.speed_x = random.randint(1, 1)
        self.speed_y = random.randint(1, 1)
        self.health = 20
        self.derniere_col = 0

    def attack(self,other_sprite):
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
            other_sprite.health -= 9
            if other_sprite.health <= 0:
                other_sprite.kill()

    def update(self):
        self.cpt += 1
        self.rect.x += self.dx * self.speed_x

        if self.rect.left < 0:
            self.dx = 1
            self.direction_x = "Est"
        
        if self.rect.right > pygame.display.get_surface().get_width():
            self.dx = -1
            self.direction_x = "Ouest"

        self.rect.y += self.dy * self.speed_y

        if self.rect.top < 0:
            self.dy = 1
            self.direction_y = "Sud"

        if self.rect.bottom > pygame.display.get_surface().get_height():
            self.dy = -1
            self.direction_y = "Nord"

        if self.dx == 1:
            self.direction_x = "Est"
        else:
            self.direction_x = "Ouest"

        if self.dy == 1:
            self.direction_y = "Sud"
        else:
            self.direction_y = "Nord"

        if self.num_image < len(images[self.direction_x]["Dragon"]):
            self.image = images[self.direction_x]["Dragon"][self.num_image]

        if self.cpt == 48:
            self.num_image = 0 if self.num_image + 1 > 4 else self.num_image + 1
            self.cpt = 0

        if random.random() < 0.01:
            self.dx = random.choice([-1, 1])
            self.dy = random.choice([-1, 1])

        colliding_sprites = pygame.sprite.spritecollide(self,self.all_sprites,False)
        for sprite in colliding_sprites:
            if sprite != self:
                self.attack(sprite)

sheet_dragon = pygame.image.load("pré_rapport/Images/Dragon.png")
height = sheet_dragon.get_height()
width = sheet_dragon.get_width() / 3

for i in range(3):
    image = sheet_dragon.subsurface([width * i, 0, width, height])
    images["Ouest"]["Dragon"].append(image)
    images["Est"]["Dragon"].append(pygame.transform.flip(image, True, False))

for j in images.keys():
    for i in range(len(images[j]["Dragon"])):
        images[j]["Dragon"][i] = pygame.transform.scale(images[j]["Dragon"][i], (60, 125))

class LapinPygame(pygame.sprite.Sprite):

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
        self.image = images[self.direction_x]["Lapin"][self.num_image]
        self.rect = self.image.get_rect()
        self.rect.x = 660
        self.rect.y = 120
        self.speed_x = random.randint(1, 1)
        self.speed_y = random.randint(1, 1)
        self.health = 2.5
        self.derniere_col = 0

    def attack(self,other_sprite):
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
            other_sprite.health -= 0.5
            if other_sprite.health <= 0:
                other_sprite.kill()

    def update(self):
        self.cpt += 1
        self.rect.x += self.dx * self.speed_x

        if self.rect.left < 0:
            self.dx = 1
            self.direction_x = "Est"
        
        if self.rect.right > pygame.display.get_surface().get_width():
            self.dx = -1
            self.direction_x = "Ouest"

        self.rect.y += self.dy * self.speed_y

        if self.rect.top < 0:
            self.dy = 1
            self.direction_y = "Sud"

        if self.rect.bottom > pygame.display.get_surface().get_height():
            self.dy = -1
            self.direction_y = "Nord"

        if self.dx == 1:
            self.direction_x = "Est"
        else:
            self.direction_x = "Ouest"

        if self.dy == 1:
            self.direction_y = "Sud"
        else:
            self.direction_y = "Nord"

        if self.num_image < len(images[self.direction_x]["Lapin"]):
            self.image = images[self.direction_x]["Lapin"][self.num_image]

        if self.cpt == 20:
            self.num_image = 1 if self.num_image + 1 > 4 else self.num_image + 1
            self.cpt = 0

        if random.random() < 0.01:
            self.dx = random.choice([-1, 1])
            self.dy = random.choice([-1, 1])
            
        collided_walls = pygame.sprite.spritecollide(self, walls, False)
        if collided_walls:
            self.rect.x -= self.dx * self.speed_x
            self.rect.y -= self.dy * self.speed_y
            self.dx = -self.dx
            self.dy = -self.dy

        collided_lacs = pygame.sprite.spritecollide(self, lac, False)
        if collided_lacs:
            self.rect.x -= self.dx * self.speed_x
            self.rect.y -= self.dy * self.speed_y
            self.dx = -self.dx
            self.dy = -self.dy

        colliding_sprites = pygame.sprite.spritecollide(self,self.all_sprites,False)
        for sprite in colliding_sprites:
            if sprite != self:
                self.attack(sprite)

sheet_lapin = pygame.image.load("pré_rapport/Images/Lapin.png")
height = sheet_lapin.get_height()
width = sheet_lapin.get_width() / 3

for i in range(3):
    image = sheet_lapin.subsurface([width * i, 0, width, height])
    images["Ouest"]["Lapin"].append(image)
    images["Est"]["Lapin"].append(pygame.transform.flip(image, True, False))

for j in images.keys():
    for i in range(len(images[j]["Lapin"])):
        images[j]["Lapin"][i] = pygame.transform.scale(images[j]["Lapin"][i], (50, 100))

class LionPygame(pygame.sprite.Sprite):

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
        self.image = images[self.direction_x]["Lion"][self.num_image]
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 200
        self.speed_x = random.randint(1, 1)
        self.speed_y = random.randint(1, 1)
        self.health = 10
        self.derniere_col = 0

    def attack(self,other_sprite):
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
            other_sprite.health -= 7.5
            if other_sprite.health <= 0:
                other_sprite.kill()

    def update(self):
        self.cpt += 1
        self.rect.x += self.dx * self.speed_x

        if self.rect.left < 0:
            self.dx = 1
            self.direction_x = "Est"
        
        if self.rect.right > pygame.display.get_surface().get_width():
            self.dx = -1
            self.direction_x = "Ouest"

        self.rect.y += self.dy * self.speed_y

        if self.rect.top < 0:
            self.dy = 1
            self.direction_y = "Sud"

        if self.rect.bottom > pygame.display.get_surface().get_height():
            self.dy = -1
            self.direction_y = "Nord"

        if self.dx == 1:
            self.direction_x = "Est"
        else:
            self.direction_x = "Ouest"

        if self.dy == 1:
            self.direction_y = "Sud"
        else:
            self.direction_y = "Nord"

        if self.num_image < len(images[self.direction_x]["Lion"]):
            self.image = images[self.direction_x]["Lion"][self.num_image]

        if self.cpt == 48:
            self.num_image = 0 if self.num_image + 1 > 1 else self.num_image + 1
            self.cpt = 0

        if random.random() < 0.01:
            self.dx = random.choice([-1, 1])
            self.dy = random.choice([-1, 1])
            
        collided_walls = pygame.sprite.spritecollide(self, walls, False)
        if collided_walls:
            self.rect.x -= self.dx * self.speed_x
            self.rect.y -= self.dy * self.speed_y
            self.dx = -self.dx
            self.dy = -self.dy

        collided_lacs = pygame.sprite.spritecollide(self, lac, False)
        if collided_lacs:
            self.rect.x -= self.dx * self.speed_x
            self.rect.y -= self.dy * self.speed_y
            self.dx = -self.dx
            self.dy = -self.dy

        colliding_sprites = pygame.sprite.spritecollide(self,self.all_sprites,False)
        for sprite in colliding_sprites:
            if sprite != self:
                self.attack(sprite)

sheet_lion = pygame.image.load("pré_rapport/Images/Lion.png")
height = sheet_lion.get_height()
width = sheet_lion.get_width() / 3

for i in range(3):
    image = sheet_lion.subsurface([width * i, 0, width, height])
    images["Ouest"]["Lion"].append(image)
    images["Est"]["Lion"].append(pygame.transform.flip(image, True, False))

for j in images.keys():
    for i in range(len(images[j]["Lion"])):
        images[j]["Lion"][i] = pygame.transform.scale(images[j]["Lion"][i], (60, 125))

class SerpentPygame(pygame.sprite.Sprite):

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
        self.image = images[self.direction_x]["Serpent"][self.num_image]
        self.rect = self.image.get_rect()
        self.rect.x = 775
        self.rect.y = 650
        self.speed_x = random.randint(1, 1)
        self.speed_y = random.randint(1, 1)
        self.health = 5
        self.derniere_col = 0

    def attack(self,other_sprite):
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
            other_sprite.health -= 2.5
            if other_sprite.health <= 0:
                other_sprite.kill()

    def update(self):
        self.cpt += 1
        self.rect.x += self.dx * self.speed_x

        if self.rect.left < 0:
            self.dx = 1
            self.direction_x = "Est"
        
        if self.rect.right > pygame.display.get_surface().get_width():
            self.dx = -1
            self.direction_x = "Ouest"

        self.rect.y += self.dy * self.speed_y

        if self.rect.top < 0:
            self.dy = 1
            self.direction_y = "Sud"

        if self.rect.bottom > pygame.display.get_surface().get_height():
            self.dy = -1
            self.direction_y = "Nord"

        if self.dx == 1:
            self.direction_x = "Est"
        else:
            self.direction_x = "Ouest"

        if self.dy == 1:
            self.direction_y = "Sud"
        else:
            self.direction_y = "Nord"

        if self.num_image < len(images[self.direction_x]["Serpent"]):
            self.image = images[self.direction_x]["Serpent"][self.num_image]

        if self.cpt == 48:
            self.num_image = 0 if self.num_image + 1 > 1 else self.num_image + 1
            self.cpt = 0

        if random.random() < 0.01:
            self.dx = random.choice([-1, 1])
            self.dy = random.choice([-1, 1])
            
        collided_walls = pygame.sprite.spritecollide(self, walls, False)
        if collided_walls:
            self.rect.x -= self.dx * self.speed_x
            self.rect.y -= self.dy * self.speed_y
            self.dx = -self.dx
            self.dy = -self.dy
	        

        colliding_sprites = pygame.sprite.spritecollide(self,self.all_sprites,False)
        for sprite in colliding_sprites:
            if sprite != self:
                self.attack(sprite)

sheet_serpent = pygame.image.load("pré_rapport/Images/Serpent.png")
height = sheet_serpent.get_height()
width = sheet_serpent.get_width() / 3

for i in range(3):
    image = sheet_serpent.subsurface([width * i, 0, width, height])
    images["Ouest"]["Serpent"].append(image)
    images["Est"]["Serpent"].append(pygame.transform.flip(image, True, False))

for j in images.keys():
    for i in range(len(images[j]["Serpent"])):
        images[j]["Serpent"][i] = pygame.transform.scale(images[j]["Serpent"][i], (50, 100))

class SourisPygame(pygame.sprite.Sprite):

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
        self.image = images[self.direction_x]["Souris"][self.num_image]
        self.rect = self.image.get_rect()
        self.rect.x = 750
        self.rect.y = 375
        self.speed_x = random.randint(1, 1)
        self.speed_y = random.randint(1, 1)
        self.health = 2
        self.derniere_col = 0

    def attack(self,other_sprite):
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
            other_sprite.health -= 1
            if other_sprite.health <= 0:
                other_sprite.kill()

    def update(self):
        self.cpt += 1
        self.rect.x += self.dx * self.speed_x

        if self.rect.left < 0:
            self.dx = 1
            self.direction_x = "Est"
        
        if self.rect.right > pygame.display.get_surface().get_width():
            self.dx = -1
            self.direction_x = "Ouest"

        self.rect.y += self.dy * self.speed_y

        if self.rect.top < 0:
            self.dy = 1
            self.direction_y = "Sud"

        if self.rect.bottom > pygame.display.get_surface().get_height():
            self.dy = -1
            self.direction_y = "Nord"

        if self.dx == 1:
            self.direction_x = "Est"
        else:
            self.direction_x = "Ouest"

        if self.dy == 1:
            self.direction_y = "Sud"
        else:
            self.direction_y = "Nord"

        if self.num_image < len(images[self.direction_x]["Souris"]):
            self.image = images[self.direction_x]["Souris"][self.num_image]

        if self.cpt == 48:
            self.num_image = 0 if self.num_image + 1 > 1 else self.num_image + 1
            self.cpt = 0

        if random.random() < 0.01:
            self.dx = random.choice([-1, 1])
            self.dy = random.choice([-1, 1])
            
        collided_walls = pygame.sprite.spritecollide(self, walls, False)
        if collided_walls:
            self.rect.x -= self.dx * self.speed_x
            self.rect.y -= self.dy * self.speed_y
            self.dx = -self.dx
            self.dy = -self.dy

        collided_lacs = pygame.sprite.spritecollide(self, lac, False)
        if collided_lacs:
            self.rect.x -= self.dx * self.speed_x
            self.rect.y -= self.dy * self.speed_y
            self.dx = -self.dx
            self.dy = -self.dy

        colliding_sprites = pygame.sprite.spritecollide(self,self.all_sprites,False)
        for sprite in colliding_sprites:
            if sprite != self:
                self.attack(sprite)

sheet_souris = pygame.image.load("pré_rapport/Images/Souris.png")
height = sheet_souris.get_height()
width = sheet_souris.get_width() / 3

for i in range(3):
    image = sheet_souris.subsurface([width * i, 0, width, height])
    images["Ouest"]["Souris"].append(image)
    images["Est"]["Souris"].append(pygame.transform.flip(image, True, False))

for j in images.keys():
    for i in range(len(images[j]["Souris"])):
        images[j]["Souris"][i] = pygame.transform.scale(images[j]["Souris"][i], (WIDTH, HEIGHT))

class OeufPygame(pygame.sprite.Sprite):
    def __init__(self,all_sprites):
        pygame.sprite.Sprite.__init__(self)
        self.all_sprites = all_sprites
        self.num_image = 0
        self.direction_x = "Ouest"
        self.direction_y = "Sud"
        self.cpt = 0
        self.dx = -1
        self.dy = 1
        self.image = images[self.direction_x]["Oeuf"][self.num_image]
        self.rect = self.image.get_rect()
        self.rect.x = 270
        self.rect.y = 700
        self.speed_x = random.randint(1, 1)
        self.speed_y = random.randint(1, 1)
        self.health = 1

    def attack(self,other_sprite):
        other_sprite.health -= 0
        if other_sprite.health <= 0:
            other_sprite.kill()

    def update(self):

        colliding_sprites = pygame.sprite.spritecollide(self,self.all_sprites,False)
        for sprite in colliding_sprites:
            if sprite != self:
                self.attack(sprite)

sheet_oeuf = pygame.image.load("pré_rapport/Images/Oeuf.png")
height = sheet_oeuf.get_height()
width = sheet_oeuf.get_width() / 3

for i in range(3):
    image = sheet_oeuf.subsurface([width * i, 0, width, height])
    images["Ouest"]["Oeuf"].append(image)
    images["Est"]["Oeuf"].append(pygame.transform.flip(image, True, False))

for j in images.keys():
    for i in range(len(images[j]["Oeuf"])):
        images[j]["Oeuf"][i] = pygame.transform.scale(images[j]["Oeuf"][i], (WIDTH, HEIGHT))

class OeufSerpentPygame(pygame.sprite.Sprite):
    def __init__(self,all_sprites):
        pygame.sprite.Sprite.__init__(self)
        self.all_sprites = all_sprites
        self.num_image = 0
        self.direction_x = "Ouest"
        self.direction_y = "Sud"
        self.cpt = 0
        self.dx = -1
        self.dy = 1
        self.image = images[self.direction_x]["OeufSerpent"][self.num_image]
        self.rect = self.image.get_rect()
        self.rect.x = 750
        self.rect.y = 650
        self.speed_x = random.randint(1, 1)
        self.speed_y = random.randint(1, 1)
        self.health = 1

    def attack(self,other_sprite):
        other_sprite.health -= 0
        if other_sprite.health <= 0:
            other_sprite.kill()

    def update(self):
        colliding_sprites = pygame.sprite.spritecollide(self,self.all_sprites,False)
        for sprite in colliding_sprites:
            if sprite != self:
                self.attack(sprite)

sheet_oeufSerpent = pygame.image.load("pré_rapport/Images/OeufSerpent.png")
height = sheet_oeufSerpent.get_height()
width = sheet_oeufSerpent.get_width() / 3

for i in range(3):
    image = sheet_oeufSerpent.subsurface([width * i, 0, width, height])
    images["Ouest"]["OeufSerpent"].append(image)
    images["Est"]["OeufSerpent"].append(pygame.transform.flip(image, True, False))

for j in images.keys():
    for i in range(len(images[j]["OeufSerpent"])):
        images[j]["OeufSerpent"][i] = pygame.transform.scale(images[j]["OeufSerpent"][i], (25, 75))

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        
# x abcisse et y ordonnée
walls = pygame.sprite.Group()
home = Wall(85, 12, 85, 90)
wall1 = Wall(0, 380, 115, 400)
wall2 = Wall(115, 550, 105, 300)
wall3 = Wall(0, 0, 40, 380)
wall4 = Wall(810, 0, 190, 330)
wall5 = Wall(725, 0, 85, 140)
wall6 = Wall(685, 0, 40, 50)
wall7 = Wall(945, 330, 55, 130)
wall8 = Wall(242, 402.5, 75, 77.5)
wall9 = Wall(40, 297, 90, 10)
wall10 = Wall(185, 297, 114, 10)
wall11 = Wall(300, 190, 3, 100)
wall12 = Wall(317, 85, 3, 105)
wall13 = Wall(338, 45, 4, 50)
wall14 = Wall(342, 45, 100, 20)
wall15 = Wall(442, 65, 65, 20)
wall16 = Wall(507, 85, 77, 20)
wall17 = Wall(584, 105, 21, 20)
wall18 = Wall(605, 105, 3, 50)
wall19 = Wall(608, 145, 16, 20)
wall20 = Wall(624, 145, 3, 110)
wall21 = Wall(607, 255, 17, 3)
wall22 = Wall(605, 255, 3, 20)
wall23 = Wall(587, 275, 20, 3)
wall24 = Wall(585, 275, 3, 22)
wall25 = Wall(545, 297, 40, 3)
wall26 = Wall(543, 297, 3, 83)
wall27 = Wall(522, 380, 23, 4)
wall28 = Wall(445, 380, 18, 3)
wall29 = Wall(443, 380, 3, 120)
wall30 = Wall(443, 501, 40, 10)
wall31 = Wall(483, 501, 3, 22)
wall32 = Wall(485, 523, 38, 7)
wall33 = Wall(523, 523, 3, 23)
wall34 = Wall(523, 546, 21, 5)
wall35 = Wall(544, 546, 3, 65)
wall36 = Wall(544, 610, 138, 13)
wall37 = Wall(682, 590, 4, 30)
wall38 = Wall(682, 587, 82, 16)
wall39 = Wall(764, 567, 82, 20)
wall40 = Wall(843, 487, 3, 100)
wall41 = Wall(843, 483, 45, 20)
wall42 = Wall(888, 483, 3, 55)
wall43 = Wall(891, 525, 37, 13)
wall44 = Wall(928, 525, 3, 170)
wall45 = Wall(929, 690, 20, 10)
wall46 = Wall(949, 690, 3, 70)
wall47 = Wall(361, 670, 3, 80)
wall48 = Wall(362, 670, 140, 3)
wall49 = Wall(502, 670, 3, 23)
wall50 = Wall(502, 693, 80, 3)
wall51 = Wall(582, 693, 3, 20)
wall52 = Wall(582, 713, 120, 3)
wall53 = Wall(702, 713, 3, 50)
walls.add(home, wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8, wall9, wall10, wall11, wall12, wall13, wall14, wall15, wall16, wall17, wall18, wall19, wall20, wall21, wall22, wall23, wall24, wall25, wall26, wall27, wall28, wall29, wall30, wall31, wall32, wall33, wall34, wall35, wall36, wall37, wall38, wall39, wall40, wall41, wall42, wall43, wall44, wall45, wall46, wall47, wall48, wall49, wall50, wall51, wall52, wall53)

class Water(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)

lac = pygame.sprite.Group()
lac1 = Water(518, 645, 67, 48)
lac2 = Water(585, 645, 82, 68)
lac3 = Water(540, 625, 107, 22)
lac.add(lac1, lac2, lac3)
