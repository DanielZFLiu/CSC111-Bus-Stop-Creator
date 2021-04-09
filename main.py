""" CSC111 Final Project: Bus Stop Creator
main.py

================================================================================
This is the main file to run the program. This will launch an interactive
pygame screen.
================================================================================
Copyright (c) 2021 Andy Wang, Varun Pillai, Ling Ai, Daniel Liu
"""
import pygame
from graph_stuff.city_classes import *
from pygame_stuff.drawing import *

WIDTH, HEIGHT = 1000, 800


def run_visualization(input_file: str = "",
                      output_file: str = "data/default_file.txt") -> None:
    """
    Run the interactive city builder. If <input_file> != "", import the city from the file.

    Controls:
      - Click to place a regular place
      - i + click to place a street intersection
      - shift + click two places to connect them by a street
      - ctrl + click to delete a street or place
      - press b to make the bus stops (ONLY DOES ANYTHING IF THERE ARE NO BUS STOPS)
      - ctrl + s to save the current city layout to the given output_file
        (does not save bus stops - in fact, the city with bus stops and the user's
        original city are different)

    Preconditions:
      - input_file and output_file, if specified, are .txt files in the data folder
      - input_file must exist if specified
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(GRASS)  # initially fill the screen with grass colour

    # misc variables for running pygame and city
    running = True

    street_pair = []  # used for adding streets; keeps track of endpoints, resets for
    # every two pairs added

    city = City()
    if input_file != "":
        # Import a city instead
        city = City.build_from_file(input_file)

    city.draw(screen)  # Draw at the start

    while running:
        # Get whatever key is pressed
        key = pygame.key.get_pressed()

        # Listen for keys that are HELD DOWN
        running = not key[pygame.K_ESCAPE]
        shift_down = key[pygame.K_LSHIFT]
        ctrl_down = key[pygame.K_LCTRL]
        i_down = key[pygame.K_i]

        # Check for user mouse input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click
                # Get the user's mouse coordinates
                mouse_pos = pygame.mouse.get_pos()

                if shift_down:  # Shift click on two places to connect a street
                    place_pos, element_type = city.get_element_from_pos(mouse_pos)

                    if place_pos is None or element_type != "Place":
                        continue
                    elif (place_pos not in street_pair) and (len(street_pair) == 0):
                        # street_pair is empty, add the first of the pair
                        street_pair.append(place_pos)
                    elif (place_pos not in street_pair) and (len(street_pair) == 1):
                        # street_pair will have two elements, completing a pair
                        # now add the street and reset street_pair
                        street_pair.append(place_pos)
                        city.add_street(street_pair[0], street_pair[1])
                        street_pair = []
                elif ctrl_down:  # Shift click on a place or a street to remove it
                    # This will be a tuple
                    element_to_delete, element_type = city.get_element_from_pos(mouse_pos)

                    if element_to_delete is None:
                        continue
                    elif element_type == "Place":
                        city.delete_place(element_to_delete)
                    else:
                        city.delete_street(element_to_delete[0], element_to_delete[1])

                elif city.get_element_from_pos(mouse_pos) == (None, None):
                    # Nothing is being held, so just add a place
                    # But do NOT add a place if the mouse is on top of an already existing place

                    # hold i to make an intersection
                    if i_down:
                        city.add_place(mouse_pos, kind='intersection')
                    else:
                        city.add_place(mouse_pos)

                # Only need to update the screen when something is added to the city
                screen.fill(GRASS)  # background colour
                city.draw(screen)
                # The advantage of doing this is that the bus stops disappear when you modify
                # the city, and that makes sense

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    # press 'b' to place bus stops
                    # TODO: add user choice for bus stop number

                    # Creates a deep copy of the city, mutates THAT, and display THAT
                    display_city = city.add_bus_stops(3)
                    screen.fill(GRASS)  # background colour
                    display_city.draw(screen)
                    # Draw this new city with the bus stops

                if event.key == pygame.K_s and ctrl_down:
                    # Ctrl + s to save the city
                    city.export_to_file(output_file)
                    print("City saved")

        pygame.display.flip()

    pygame.display.quit()


if __name__ == "__main__":
    run_visualization("data/default_file")
