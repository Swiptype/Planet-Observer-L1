# -*- coding: utf-8 -*-

import random
import turtle


class Grid:

    def __init__(self, grid_init):
        """ Classe 'Grid' avec 3 attributs :
                - 'grid' : initialisé avec le paramètre 'grid_init'
                - 'lines_count' : initialisé avec le nombre de lignes de 'grid_init'
                - columns_count' : initialisé avec le nombre de colonnes de 'grid_init'."""
        self.grid = grid_init
        self.lines_count = len(grid_init)
        self.columns_count = len(grid_init[0]) if len(grid_init) else 0

    def fill_random(self, values):
        """ Rempli la grille de valeurs aléatoires de la liste 'values'"""
        self.grid = [[random.choice(values)
                      for _ in range(self.columns_count)]
                     for _ in range(self.lines_count)]

    def get_line(self, line_number):
        """ Extrait la ligne numéro 'line_number' de la grille."""
        return self.grid[line_number]

    def get_column(self, column_number):
        """ Extrait la colonne numéro 'column_number' de la grille."""
        return [line[column_number] for line in self.grid]

    def get_line_str(self, line_number, separator='\t'):
        """ Retourne la chaine de caractère correspondant à la concaténation des valeurs de la ligne numéro
        'line_number' de la grille. Les caractères sont séparés par le caractère 'separator'."""
        return separator.join(str(value)
                              for value in self.grid[line_number])

    def get_grid_str(self, separator='\t'):
        """ Retourne la chaine de caractère représentant la grille.
                Les caractères de chaque ligne sont séparés par le caractère 'separator'.
                Les lignes sont séparées par le caractère de retour à la ligne '\n'."""
        return '\n'.join(self.get_line_str(line_number, separator)
                         for line_number in range(self.lines_count))

    def get_diagonal(self):
        """ Extrait la diagonale de la grille."""
        diagonal_size = min(self.lines_count, self.columns_count)
        return [self.grid[line_number][line_number]
                for line_number in range(diagonal_size)]

    def get_anti_diagonal(self):
        """ Extrait l'antidiagonale de la grille."""
        diagonal_size = min(self.lines_count, self.columns_count)
        return [self.grid[line_number][self.columns_count - line_number - 1]
                for line_number in range(diagonal_size)]

    def has_equal_values(self, value):
        """ Teste si toutes les valeurs de la grille sont égales à 'value'."""
        return all([all([grid_value == value
                         for grid_value in line])
                    for line in self.grid])

    def is_square(self):
        """ Teste si la grille a le même nombre de lignes et de colonnes."""
        return self.lines_count == self.columns_count

    def get_count(self, value):
        """ Compte le nombre d'occurrences de 'value' dans la grille."""
        return sum(line.count(value) for line in self.grid)

    def get_coordinates_from_cell_number(self, cell_number):
        """ Converti un numéro de case 'cell_number' de la grille vers les coordonnées (ligne, colonne)
        correspondants."""
        return cell_number // self.columns_count, cell_number % self.columns_count

    def get_cell_number_from_coordinates(self, line_number, column_number):
        """ Converti les coordonnées ('line_number', 'column_number') de la grille vers le numéro de case
        correspondant."""
        return line_number * self.columns_count + column_number

    def get_cell(self, cell_number):
        """ Extrait la valeur de la grille en position 'cell_number'."""
        line_number, column_number = self.get_coordinates_from_cell_number(cell_number)
        return self.grid[line_number][column_number]

    def set_cell(self, cell_number, value):
        """ Positionne la valeur 'value' dans la case 'cell_number' de la grille."""
        line_number, column_number = self.get_coordinates_from_cell_number(cell_number)
        self.grid[line_number][column_number] = value

    def get_same_value_cell_numbers(self, value):
        """ Fourni la liste des numéros des cases à valeur égale à 'value' dans la grille."""
        return [cell_number
                for cell_number in range(self.lines_count * self.columns_count)
                if self.get_cell(cell_number) == value]

    def get_neighbour(self, line_number, column_number, delta, is_tore=True):
        """ Retourne le voisin de la cellule ('line_number', 'column_number') de la grille. La définition de voisin
        correspond à la distance positionnelle indiquée par le 2-uplet 'delta' = (delta_ligne, delta_colonne). La case
        voisine est alors (ligne + delta_ligne, colonne + delta_colonne).
                Si 'is_tore' est à 'True' le voisin existe toujours en considérant la grille comme un tore.
                Si 'is_tore' est à 'False' retourne 'None' lorsque le voisin est hors de la grille."""
        new_line_number, new_column_number = line_number + delta[0], column_number + delta[1]
        if is_tore:
            return self.grid[new_line_number % self.lines_count][new_column_number % self.columns_count]
        if 0 <= new_line_number < self.lines_count and 0 <= new_column_number < self.columns_count:
            return self.grid[new_line_number][new_column_number]
        return None

    def get_neighborhood(self, line_number, column_number, deltas, is_tore=True):
        """ Retourne la liste des N voisins de la position ('lins_number', 'column_number') dans la grille correspondant
         aux N 2-uplet (delta_ligne, delta_colonne) fournis par la liste deltas.
                Si 'is_tore' est à 'True' le voisin existe toujours en considérant la grille comme un tore.
                Si 'is_tore' est à 'False' un voisin hors de la grille n'est pas considéré."""
        return [self.get_neighbour(line_number, column_number, delta, is_tore)
                for delta in deltas]

    def draw_with_turtle(self, cell_size=50, margin=50, show_values=True):
        """ Dessine avec le module 'turtle' la grille centrée avec 'margin' pixels de marge. Les cases ont une taille de
        'cell_size' pixels. Les valeurs de la grille sont affichées au centre de chaque case uniquement si 'show_values'
        a pour valeur 'True'."""
        grid_width, grid_height = cell_size * self.columns_count, cell_size * self.lines_count
        turtle.setup(grid_width + 2 * margin, grid_height + 2 * margin)
        turtle.title(f"grille de {self.lines_count} lignes et {self.columns_count} colonnes")
        turtle.speed(0)
        for cell_number in range(self.lines_count * self.columns_count):
            line_number, column_number = self.get_coordinates_from_cell_number(cell_number)
            cell_center_x = -grid_width // 2 + cell_size // 2 + column_number * cell_size
            cell_center_y = grid_height // 2 - cell_size // 2 - line_number * cell_size
            if show_values:
                turtle.up()
                turtle.goto(cell_center_x, cell_center_y)
                turtle.down()
                turtle.write(self.get_cell(cell_number))
            if line_number == 0:
                cell_top_left_x = cell_center_x - cell_size // 2
                cell_top_left_y = cell_center_y + cell_size // 2
                turtle.up()
                turtle.goto(cell_top_left_x, cell_top_left_y)
                turtle.down()
                turtle.goto(cell_top_left_x, cell_top_left_y - grid_height)
            if column_number == 0:
                cell_top_left_x = cell_center_x - cell_size // 2
                cell_top_left_y = cell_center_y + cell_size // 2
                turtle.up()
                turtle.goto(cell_top_left_x, cell_top_left_y)
                turtle.down()
                turtle.goto(cell_top_left_x + grid_width, cell_top_left_y)
        turtle.up()
        turtle.goto(grid_width // 2, grid_height // 2)
        turtle.down()
        turtle.goto(grid_width // 2, grid_height // 2 - grid_height)
        turtle.up()
        turtle.goto(-grid_width // 2, -grid_height // 2)
        turtle.down()
        turtle.goto(-grid_width // 2 + grid_width, -grid_height // 2)
        turtle.exitonclick()


if __name__ == '__main__':
    random.seed(1000)  # Permet de générer toujours le 'même' hasard pour les tests

    # Constantes de directions
    NORTH, EAST, SOUTH, WEST = (-1, 0), (0, 1), (1, 0), (0, -1)
    NORTH_EAST, SOUTH_EAST, SOUTH_WEST, NORTH_WEST = (-1, 1), (1, 1), (1, -1), (-1, -1)
    CARDINAL_POINTS = (NORTH, EAST, SOUTH, WEST)
    WIND_ROSE = (NORTH, NORTH_EAST, EAST, SOUTH_EAST, SOUTH, SOUTH_WEST, WEST, NORTH_WEST)

    # Constantes de test
    LINES_COUNT_TEST, COLUMNS_COUNT_TEST = 5, 7
    LINE_NUMBER_TEST, COLUMN_NUMBER_TEST = 1, 6
    VALUE_TEST = 0
    VALUES_TEST = list(range(2))
    IS_TORE_TEST = True
    DIRECTION_TEST = EAST
    GRID_INIT_TEST = [[VALUE_TEST] * COLUMNS_COUNT_TEST
                      for _ in range(LINES_COUNT_TEST)]
    CELL_SIZE_TEST = 100
    MARGIN_TEST = 20
    SHOW_VALUES_TEST = True

    # Tests
    grid_const = Grid(GRID_INIT_TEST)
    grid_random = Grid(GRID_INIT_TEST)
    grid_random.fill_random(VALUES_TEST)
    print(grid_const.grid)
    print(grid_random.grid)
    print(grid_random.lines_count, grid_random.columns_count)
    print(grid_random.get_line(LINE_NUMBER_TEST))
    print(grid_random.get_column(COLUMN_NUMBER_TEST))
    print(grid_random.get_line_str(2))
    print(grid_random.get_grid_str(''))
    print(grid_random.get_diagonal())
    print(grid_random.get_anti_diagonal())
    print(grid_random.has_equal_values(GRID_INIT_TEST[0][0]))
    print(grid_const.has_equal_values(GRID_INIT_TEST[0][0]))
    print(grid_random.is_square())
    print(grid_random.get_coordinates_from_cell_number(13))
    print(grid_random.get_cell_number_from_coordinates(LINE_NUMBER_TEST, COLUMN_NUMBER_TEST))
    print(grid_random.get_cell(9))
    grid_random.set_cell(9, 1)
    print(grid_random.get_cell(9))
    print(grid_random.get_same_value_cell_numbers(1))
    print(grid_random.get_neighbour(LINE_NUMBER_TEST, COLUMN_NUMBER_TEST, DIRECTION_TEST, IS_TORE_TEST))
    print(grid_random.get_neighbour(LINE_NUMBER_TEST, COLUMN_NUMBER_TEST, DIRECTION_TEST, not IS_TORE_TEST))
    print(grid_random.get_neighborhood(LINE_NUMBER_TEST, COLUMN_NUMBER_TEST, WIND_ROSE, IS_TORE_TEST))
    print(grid_random.get_neighborhood(LINE_NUMBER_TEST, COLUMN_NUMBER_TEST, WIND_ROSE, not IS_TORE_TEST))
    grid_random.draw_with_turtle(CELL_SIZE_TEST, MARGIN_TEST, SHOW_VALUES_TEST)
