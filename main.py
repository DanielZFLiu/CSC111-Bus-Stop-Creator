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
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(GRASS)  # initially fill the screen with grass colour

    # misc variables for running pygame and city
    running = True
    shift_down = False  # whether the left shift key is down
    ctrl_down = False  # whether the left control key is down
    i_down = False  # whether the i key is being held down

    street_pair = []  # used for adding streets; keeps track of endpoints, resets for
    # every two pairs added

    city = City()

    while running:
        # Get whatever key is pressed
        key = pygame.key.get_pressed()

        # Listen for keys
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

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:  # press 'b' to place bus stops
                    # TODO: add user choice for bus stop number
                    # TODO: currently pressing b more than once will break the program; fix?
                    bus_stops = city.get_bus_stops(3)

                    for bus_stop in bus_stops:
                        city.bus_stop_projected(bus_stop)

            screen.fill(GRASS)
            city.draw(screen)

        pygame.display.flip()

    pygame.display.quit()
