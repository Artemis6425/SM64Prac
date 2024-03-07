#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
#import ctypes
#ctypes.windll.kernel32.SetConsoleTitleW("SM64 Practice Script")
import random
import json
from getch import getch, pause
from pick import pick
from colorama import init, Fore, Back, Style

with open('stage.json', 'r') as sfile:
    stage_json = json.load(sfile)

# Clears text on Windows/Linux/MacOS.
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

# This function is the key used by sort() below, to sort the results by the order you would encounter them in a run, depending on the chosen category. i is the index number, for example lakitu skip would be 0.
def stage_order(course):
    try:
        i = stage_json["course-master-list"].keys().index(course)
    except:
        i = -1
    return i

# This function is how users pick which route they use. This reads from the routes defined in `stage.json`
def route_picker(category):
    category_options = list(stage_json[category].keys())
    while(1):
        option, index = pick(category_options, "Which route do you use?", indicator='>>')
        return option

# This function gets the proper weights of all the stars in the route, based off of the `course-master-list`
def get_thing(category, route):
    temp_stage = stage_json[category][route]
    temp_weight = []
    x = [temp_stage, temp_weight]
    for i in temp_stage:
        temp_weight.append(stage_json["course-master-list"][i])
    return x

# Roll to choose the course/star, handle multiple rolls (max 10), go back to the main menu, and handle any input errors.
def course_roll(course_list, category, weight_list):
    while(1):
        print(Fore.BLUE + "-" * 43)
        print(Fore.GREEN + "Type 'r' to roll (returns 1 result).")
        print("Type 'r2'-'r10' to return multiple results.")
        print(Fore.MAGENTA + "Type 'm' to go back to category selection." + Style.RESET_ALL)
        user_response = input("")
        user_response_firstchar = user_response[:1]
        clear()
        if user_response_firstchar == 'r':
            number_of_rolls = user_response[1:]

            # If misc_option is disabled, this will appropriately remove all MISC tasks from the list
            if misc_option:
                new_course_list = course_list
                new_weight_list = weight_list
            else:
                new_course_list = []
                new_weight_list = []
                j = 0
                for i in course_list:
                    if "MISC" not in i:
                        new_course_list.append(i)
                        new_weight_list.append(weight_list[j])
                    j += 1

            # This now also makes sure the max also is not above the amount of valid entries in `course_list`
            try:
                number_of_rolls = int(number_of_rolls)
                number_of_rolls = min(number_of_rolls, 10)
                number_of_rolls = max(number_of_rolls, 1)
                number_of_rolls = min(number_of_rolls, len(new_course_list))
            except:
                number_of_rolls = 1
            generated_courses = []

            #Math is here, this is a random selection that is weighted, and then checks against the generated course list to prevent duplicates. See the above defined stage_order function for how the sorting is handled.
            while len(generated_courses) < number_of_rolls:
                generated_choice = random.choices(new_course_list, new_weight_list, k=1)
                generated_choice = generated_choice[0]
                if generated_choice not in generated_courses:
                    generated_courses.append(generated_choice)
                generated_courses.sort(key=stage_order)
            print("Category:")
            print(Fore.YELLOW + category)
            print(Fore.WHITE + "Results:")
            for course_result in generated_courses:
                print(Fore.CYAN + course_result + Style.RESET_ALL) 
        elif user_response == 'm':
            break
        else:
            print("Category:")
            print(Fore.YELLOW + category)
            print(Fore.WHITE + "Results:")
            print(Fore.RED + "Error: Unknown input." + Style.RESET_ALL)

# Menu is from the imported pick library. 
title = ("Select a main category, or option to continue.")
options = ["120 Star", "70 Star", "16 Star", "1 Star", "0 Star", "MISC - DISABLED", "How To Add Routes", "About", "Quit"]
misc_option = False


while(1):
    clear()
    option, index = pick(options, title, indicator='>>')

    if " Star" in option:
        if len(stage_json[option].keys()) > 1:
            route = route_picker(option)
        else:
            route = list(stage_json[option].keys())[0]
        stage = get_thing(option, route)
        course_roll(category=option, course_list=stage[0], weight_list=stage[1])

    # This checks if user selects the "MISC" option, and toggles it
    if "MISC - " in option:
        if option == "MISC - ENABLED":
            options[5] = "MISC - DISABLED"
            misc_option = False
        else:
            options[5] = "MISC - ENABLED"
            misc_option = True

    # Script routes section (this is completely unfinished), pause is from imported getch library.
    if option == "How To Add Routes":
        pause('''How To Add Routes\n\nEffectively, you\'ll need to create your own (or copy from somebody else) from the stage.json file.
If you open the \'stage.json\' file, you\'ll see categories, then routes in a specific structure.
I would recommend copying and pasting the route that you want to make changes to, and then from there, you want to copy\\paste the star names from the \'course-master-list\'.
Once you\'ve created the route you wanted, make sure to save, and then reload this program. Your new route should show up when you click the category!
\n\nPress any key to continue.''')
        clear()

    # Script about section, pause is from imported getch library.
    if option == "About":
        pause('''SM64 Practice Script maintained by Kyman (@Kym4n)
\nCurrent Version: 0.2 beta-03-07-2024
\nChange Log:
\nVersion 0.2:
    - Implemented route functionality through the new 'stage.json' file
    - Added 'MISC' option to home menu
    - Simplified code
\nVersion 0.1.1:
    - Fixed 70 Star related bugs and adjusted weighting
    - Laid out initial idea for Routes section
    - Changed 120 Star to carpetless and 100c + cannon (until further implementation of the Routes feature)
\nVersion 0.1:
    - Created the script! Basic menu, supports all main categories and commonly used operating systems
\nThanks to these people to support/inspiration:
    - wermi (for help/teaching me Python related stuff!)
    - tayyip (for continued moral support)
    - !whichstar command from SM64 discord
    - Zombie (random star webapp)
    - Usamune (random stage per category function)
    - Artemis (for implementing 0.2)
\nPress any key to continue.''')
        clear()

    # Quit option, pause is from imported getch library.
    if option == "Quit":
        pause('Thank you so much for-a running my script. Press any key.')
        clear()
        quit()

# Script Future Ideas:
# -> format look of text better
# -> implement menus for picking route stuff, way to save settings?
# -> auto roll every x mins i.e. a10 and you do 10 mins on each star
# -> implement presets for RTA vs consistency practice, goals given change base on selection
# -> implement scaling for users pbs, prompts to enter pb, goal star times balanced to your level, "estimated good practice under xx.xx 5x"
# -> implement being able to pull from the spreadsheet the records and ideal run times (with vid links too?)
# -> tracking of your best and average time?
# -> implement routing/menu glitch related stuff for each category, access this from Routes menu option? <- WIP
