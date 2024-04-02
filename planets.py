from grid import Grid
from elements import Ground
from elements import Element

import turtle
import pygame
from mainPygame1 import *

from pygame.locals import *

class PlanetAlpha(Grid):

    NORTH = (-1,0)
    EAST = (0,1)
    SOUTH = (1,0)
    WEST = (0,-1)
    NORTH_EAST = (-1,1)
    SOUTH_EAST = (1,1)
    SOUTH_WEST = (1,-1)
    NORTH_WEST = (-1,-1)
    CARDINAL_POINTS = (NORTH,EAST,SOUTH,WEST)
    WIND_ROSE = (NORTH,NORTH_EAST,EAST,SOUTH_EAST,SOUTH,SOUTH_WEST,WEST,NORTH_WEST)
    current_animals_count = 0
    ground = Ground()
    Element = Element

    def __init__(self,longitude_cells_count,latitude_cells_count,ground):
        super().__init__(longitude_cells_count, latitude_cells_count, ground)
        self.ground = ground
        self.current_animals_count = 0
        self.elements = {}

    def add_element(self, cell_number, element):
        if self.is_free_place(cell_number):
            self.elements[cell_number] = element
            return True
        else:
            return False

    def remove_element(self, cell_number):
        if cell_number in self.elements:
            del self.elements[cell_number]
            return True
        else:
            return False

    def get_current_animals_count(self):
        return self.current_animals_count

    def incr_current_animals_count(self):
        self.current_animals_count += 1

    def decr_current_animals_count(self):
        self.current_animals_count -= 1

    def get_ground(self):
        return self.ground

    def is_free_place(self, cell_number):
        return self.get(cell_number) is None

    def get_random_free_place(self):
        free_cells = [cell_number for cell_number in self.cell_numbers() if self.is_free_place(cell_number)]
        if free_cells:
            return self.random.choice(free_cells)
        else:
            return None

    def place_resources(self, resources):
        for resource in resources:
            cell_number = self.get_random_free_place()
            if cell_number is not None:
                self.set(cell_number, resource)

    def place_animals(self, animals):
        for animal in animals:
            cell_number = self.get_random_free_place()
            if cell_number is not None:
                self.set(cell_number, animal)
                self.incr_current_animals_count()

    def get_grid_char_repr(self):
        grid_repr = ""
        for i in range(self.latitude_cells_count):
            for j in range(self.longitude_cells_count):
                cell_number = self.get_cell_number((i, j))
                if cell_number in self.elements:
                    grid_repr += str(self.elements[cell_number])
                else:
                    grid_repr += str(self.ground.get_cell((i, j)))
                if j < self.longitude_cells_count - 1:
                    grid_repr += " "
            if i < self.latitude_cells_count - 1:
                grid_repr += "\n"
        return grid_repr


    def get_count(self, value):
        count = 0
        for cell_number in self.cell_numbers():
            if self.get(cell_number) == value:
                count += 1
        return count

    def get_same_value_cell_numbers(self, value):
        return [cell_number for cell_number in self.cell_numbers() if self.get(cell_number) == value]

    def get_line_str(self, line_number, separator):
        return separator.join([Element.to_char(self.get(cell_number)) for cell_number in self.line_cell_numbers(line_number)])

    def draw_with_turtle(self, cell_size, margin, show_values):
        window = turtle.Screen()
        window.title("PlanetAlpha")
        turtle.speed(0)
        turtle.hideturtle()

        window_width = self.longitude_cells_count * cell_size + margin * 2
        window_height = self.latitude_cells_count * cell_size + margin * 2
        grid_width = self.longitude_cells_count * cell_size
        grid_height = self.latitude_cells_count * cell_size

        turtle.penup()
        turtle.goto(-window_width/2 + margin, window_height/2 - margin)
        turtle.pendown()
        turtle.color("black")
        turtle.pensize(2)

        for i in range(self.latitude_cells_count + 1):
            turtle.goto(-window_width/2 + margin, window_height/2 - margin - i * cell_size)
            turtle.goto(-window_width/2 + margin + grid_width, window_height/2 - margin - i * cell_size)
        
        turtle.penup()
        turtle.goto(-window_width/2 + margin, window_height/2 - margin)
        turtle.pendown()

        for i in range(self.longitude_cells_count + 1):
            turtle.goto(-window_width/2 + margin + i * cell_size, window_height/2 - margin)
            turtle.goto(-window_width/2 + margin + i * cell_size, window_height/2 - margin - grid_height)

        for i in range(self.latitude_cells_count):
            for j in range(self.longitude_cells_count):
                value = self.ground[i][j]
                turtle.penup()
                turtle.goto(-window_width/2 + margin + j * cell_size, window_height/2 - margin - (i + 1) * cell_size)
                turtle.pendown()
                turtle.fillcolor(value.color)
                turtle.begin_fill()
                turtle.setheading(0)
                turtle.forward(cell_size)
                turtle.right(90)
                turtle.forward(cell_size)
                turtle.right(90)
                turtle.forward(cell_size)
                turtle.right(90)
                turtle.forward(cell_size)
                turtle.end_fill()

                if show_values:
                    turtle.penup()
                    turtle.goto(-window_width/2 + margin + j * cell_size + cell_size/2, window_height/2 - margin - (i + 1) * cell_size + cell_size/2)
                    turtle.write(str(value.count), align="center", font=("Arial", 8, "normal"))

        turtle.hideturtle()
        window.mainloop()


class PlanetPygame:
    def __init__(self, name, width, height):
        pygame.init()
        self.__screen = pygame.display.set_mode((width, height))
        self.__clock = pygame.time.Clock()
        self.__name = name
        self.__screen = background
        self.__width = width
        self.__height = height
        self.all = pygame.sprite.Group()
        self.animals = pygame.sprite.Group()
        self.ressources = pygame.sprite.Group()
        self.humains = pygame.sprite.Group()
                                                                                    #Penser à faire : Animal1 = celui qui arrive sur la case de animal2
    def ajout(self, elements):
        for entites in elements:
            entites.rect.x = random.randint(0, self.__width)
            entites.rect.y = random.randint(0, self.__height)
            self.all.ajout(entites)
            if isinstance(entites, Resource):
                self.ressources.ajout(entites)
            if isinstance(entites, Animal):
                self.animals.ajout(entites)
            if isinstance(entites, Humain):
                self.humains.ajout(entites)