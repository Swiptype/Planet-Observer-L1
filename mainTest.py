import random

from config import *
from elements import *
#from planets import PlanetAlpha

""" elements.py:

print(Element('Elem', 'X'))
print(Element('Elem', 'Y'))

print(Ground())

print(Resource('Water','W',10))

a = Animal('Dragon','D',30)
a.ageing()
a.losing_life(10)
a.recovering_life(5)
print(a)

print(Herb())
print(Water())
print(Mouse())
print(Lion())
print(Cow())
a = Dragon()
a.ageing()
a.losing_life(10)
print(a)
print(Serpent())
print(Chevalier())
print(Homme())
print(Lapin())


print(Mouse().get_id() == Mouse().get_id())
print(Mouse() == Mouse())
print(Mouse() == Lion())


Fichier planets:


if __name__ == "__main__":
    random.seed(1000)
    
    planet = PlanetAlpha("Terre", PLANET_LONGITUDE_CELLS_COUNT, PLANET_LATITUDE_CELLS_COUNT, Ground())
    planet.place_resources([Herb() for _ in range(HERBS_COUNT)])
    planet.place_resources([Water() for _ in range(WATERS_COUNT)])
    planet.place_animals([Lion() for _ in range(LIONS_COUNT)])
    planet.place_animals([Dragon() for _ in range(DRAGONS_COUNT)])
    planet.place_animals([Cow() for _ in range(COWS_COUNT)])
    planet.place_animals([Mouse() for _ in range(MOUSES_COUNT)])

    print(planet.get_grid_str())
    h , w , l , d , c , m, g = Herb(), Water(), Lion(), Dragon(), Cow(), Mouse(), Ground()
    print(f"La planète{planet.get_name()} a {planet.get_lines_count() * planet.get_column_count()} places", end = "")
    print(f"avec {planet.get_current_animals_count()} animaux qui s’y baladent : ")
    for element in(h, w, l, d, c, m, g):
        print(f"\t{planet.get_count(element)} {element.get_name()} : {planet.get_same_value_cell_numbers(element)}")
    dragon_cell_number = planet.get_same_value_cell_numbers(d)[0]
    line_dragon, column_dragon = planet.get_coordinates_from_cell_number(dragon_cell_number)
    print(f"\tLe voisinage de {d.get_char_repr()} aux points cardinaux est: ",end = "")
    print([element.get_char_repr()
    for element in planet.get_neighborhood(line_dragon, column_dragon, planet.CARDINAL_POINTS, True)])
    print(f"\tLe voisinage complet de {d.get_char_repr()} est :",end = "")
    print([element.get_char_repr()
    for element in planet.get_neighborhood(line_dragon, column_dragon, planet.WIND_ROSE, True)])
    planet.draw_with_turtle(PLANET_CELL_PIXEL_SIZE)


nouvel_animal = Animal("Lion", "\U0001F981", 15, "Lion",10)
#autre_animal=Animal("Marguerite", "l2", 16, "Cow")
autre_animal=Animal("Lionel", "\U0001F981", 16, "Lion",10)

nouvel_animal2 = Animal("Serpent", "\U0001F40D", 5, "Serpent",2)
autre_animal2=Animal("Lionel", "\U0001F40D", 6, "Serpent",2)

#print(nouvel_animal.apparition_animal(autre_animal))

print(nouvel_animal.__repr__())
print(autre_animal.__repr__())
print(nouvel_animal2.__repr__())
print(autre_animal2.__repr__())

nouvel_animal.apparition_animal(autre_animal)
nouvel_animal2.apparition_animal(autre_animal2)

nouvel_animal3 = nouvel_animal
autre_animal3 = autre_animal

print(nouvel_animal3.apparition_animal(autre_animal3))

nouvel_humain = Humain("Damien", "\U0001F64D" , 10, "Humain", 5)
autre_humain = Humain("Louise", "\U0001F64D" , 10, "Humain", 5)

print(nouvel_humain.apparition_humain(autre_humain))
"""

nouvel_animal = Animal("Serpent", "\U0001F40D", 8, "Serpent", 2)
#print("Serpent : ", nouvel_animal)

autre_animal = Animal("Lion", "\U0001F981", 10, "Lion", 7.5)
#print("Lion : ", autre_animal)

print(Animal.duel(nouvel_animal, autre_animal))