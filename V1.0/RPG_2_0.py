# Program Name: A mess tide together
# Author: Zach Moore
# Class: CSIS 155
# Assignment: 06
# Due Date: 10/15/2024
# Description: A basic model of functions and classes used to
# create a very basic and function version of an RPG 


import sys
import random
from Basic_Functions import yesno_loop, choice_num_loop, print_choice
from RPG_3_class import Scene, Object, Player, goblin

runs = 0

## SECTION ##
def WT_Tutorial():
    """ Run the tutorial"""
    temp_name = input("Welcome to Veliam, what is your name? (12 chr limit)")
    #Player creation
    hero = Player(30, 30, temp_name[0:16:1], [])
    print (f"Well {hero.name} you've found yourself in my tower, take a look around")
    temp_answer = yesno_loop(input("Take a look around? Y/N: "),\
                              "Take a look around? Y/N: ")
    temp_index = 0
    # Would'nt like to look around, will run through the list then print ...
    while (temp_answer == 0):
        wizard_list = ["To spite the wizard you close your eyes",
                        "You hear disturbed wizard mumbles",
                        "You're really showing it to the man huh",
                          "You and the wizard, wait... in silence",
                        "...", "...", "...",
                          "you feel the floor beneath your feet",
                            "It's a cold floor",
                        "...", "yep. cold floor", "something feels wrong",
                          "A deep low disturbance grows in your chest",
                        "You Burp", "...", "Taste's like...\nchicken?"]
        if (temp_index < len(wizard_list)):
            print(wizard_list[temp_index])
        else:
            print("...")
        temp_index += 1
        temp_answer = yesno_loop(input("Would you like to leave? Y/N: "),\
                                  "Would you like to leave? Y/N: ")
    print(" A large room lays before you a kindly wizard waiting by the door,",
          " \n a deep black stone is what makes up most of walls and floor.\n",
        "A massive cauldron in the center of the room",
        " bubbles pleasantly, Alongside this a weapons rack\n",
        "which holds a pretty cool looking sword\n")

    ####
    # below are the object and scenes needed to run the while loop
    ####
    # tracks choices made to get rid of cheese tracker, exit determines when
    # the player has grabbed a weapon they may leave
    # and the menu is what the player will be able to chose from
    WT_explore = Scene({"choices" : 0, "exit" : 0, 
                "menu": {"The cauldron" : 1, "The weapons rack" : 2,\
                         "The window" : 3,"Cheese?" : 4}})
    # this is a menu and tracker to be used i=on the weapons rack
    WT_trackers = Scene({"MACE" : 0, "DAGGER" : 0, "SWORD" : 0,})
    # tracks if cauldron has been looted
    cauldron = Object("POTION", 1)
    
        # TOP OF WIZARD TOWER
    # this code will run until the player selects the exit
    while True:
        # the below code determines if the player has grabbed a weapon
        # and if so will add exit to the players choices
        if WT_explore.return_value("choices") == 3:
            WT_explore.update("exit", 1)
            WT_explore.update_menu("The exit", 4)
        # the below code prints the menu and grabs a user choice
        print_choice(WT_explore.return_value("menu"))
        temp_input = input("Pick a choice: ")
        temp_choice = choice_num_loop(WT_explore.return_value("menu"), temp_input)
        # this code is what deletes cheese? option after the first choice and
        # manages the choice giving the player the item cheese and a dairy-
        #funny prompt
        if temp_choice == 4 and ("Cheese?" in WT_explore.interactions["menu"]):
            print("You have chosen a path you can not return from, may god have mercy",
                " on your soul")
            hero.looting([1,"MOON CHEESE"])
            del WT_explore.interactions["menu"]["Cheese?"]
        elif "Cheese?" in WT_explore.interactions["menu"]:
            del WT_explore.interactions["menu"]["Cheese?"]
        # Weapons rack

        if temp_choice == 2:
            # 1 : ["name", die #, die type, Hit bonus, damage bonus]
            # this is the format of a weapon
            rack_weapons_dict_details = { 1 : ["MACE", 1, 8, 2, 10],
                                        2 : ["DAGGER", 1, 4, 10, 4],
                                        3 : ["SWORD", 1, 6, 5, 6]}
            rack_weapons_dict = {"MACE" : 1, "DAGGER" : 2, "SWORD" : 3}
            rack_weapons_menu = {}
            
            print("A large rack of weapons lays before you,"
                  " seemingly untouched in years\n",
                "As evidenced by the layer of dust ",
                "adorning it. You find...\n\n")
            # the below code inefficient and could be shortened if I created
            # a scene object to keep track of the weapons, what the below code
            # does is checks what if any weapons the user has grabbed and
            # creates a dict accordingly
            temp_check = 0
            temp_tracker = 1
            for key, value in rack_weapons_dict.items():
                if WT_trackers.interactions[key] == 0:
                    value = temp_tracker
                    rack_weapons_menu[key] = temp_tracker
                    temp_tracker += 1
                    temp_check += 1

            # makes sure the EXIT option will be numbered correctly
            rack_weapons_menu["EXIT"] = len(rack_weapons_menu) + 1
            
            # temp check tracks remaining weapons
            if temp_check > 1:
                print("A wide array of weapons to choose from!")
            elif temp_check == 1:
                print("A single weapon left")
            elif temp_check == 0:
                print("There are no weapons left,"
                      " Congrats you've robbed an old man!")

            print_choice(rack_weapons_menu)
            # below is a menu manager for weapon choices
            temp_input = input("\nMake a choice: ")
            temp_input = choice_num_loop(rack_weapons_menu, temp_input)
            # exit option will always be last on rack_weapon_menu
            if temp_input == len(rack_weapons_menu):
                print("Exiting weapon selection.")
            else:
                # grabs weapon name, to use in a print statement and a key 
                # search
                weapon_name = list(rack_weapons_menu.keys())[temp_input - 1]
                print(f"You have taken the {weapon_name}")
                # tracker to show which weapon was taken
                WT_trackers.interactions[weapon_name] = 1
                # creates a list from a dictionary, making a weapon list
                weapon_details = []
                for value in rack_weapons_dict_details.values():
                    if value[0] == weapon_name:
                        weapon_details = value
                        break
                # gives player chosen weapon
                hero.loot_weapon(weapon_details)
                # shows user their inventory after
                hero.inventory()
                # if a weapon has been taken it will update main menu with exit
                if len(WT_explore.interactions["menu"]) <= 3:
                    WT_explore.update_menu("EXIT", 4)

        if temp_choice == 1:
            # cauldron amount tracks if the potion has been taken
            if cauldron.amount == 1:
                print("As you approach the boiling cauldron",
                      " you see next to it a shelf adorned with a red potion")
                print()
                temp_answer = input("Will you take it? Y/N? ")
                temp_answer = yesno_loop(temp_answer)
                if temp_answer == 1:
                    print("You quickly stash the potion and move along")
                    hero.looting(cauldron.looted())
                elif temp_answer == 0:
                    print("The wizard seems disappointed as you walk away")
            elif cauldron.amount == 0:
                print("It seems there nothing left for you here")
            input("Continue? ")
        # window
        if temp_choice == 3:
            print(f"You look across a vast valley in a unfamiliar land, none of this seems familiar to you")
        # used to determine how many times the menu has been used, to get rid of cheese after the first
        global runs
        runs += 1
        if temp_choice == 4 and  (runs >= 2):
            print("feeling ready, you head towards the door")
            break
    # Combat time
    print("The wizard smiles at you as you approach\n'I'm surprised You'be made it this far, I'm",
          "not sure if you noticed but this whole world was very conceptual at base\nThere's a town probably a few weeks",
          "out from possible development, so in the meantime\n",
          "I'm gonna make you fight some goblins to the death, good luck :/'\n")
    print("We do not like the wizard")

    print("You unceremoniously get throw down a flight of stairs and observe a polite line of goblins waiting to kill you")
    
    print("ROUND 1\n")
    print("A pretty skimpy looking goblin walks up to you")
    goblin1 = goblin("Wretch")
    while hero.HP > 0 and goblin1.alive:
        hero.combat_menu(goblin1)
        goblin1.attack(hero)
    print("One kill? Not too bad.\nLets make this fight a bit more even")
    print("ROUND 2\n")
    goblin2 = goblin("guy", "Medium", 20, 20)
    while hero.HP > 0 and goblin2.alive:
        hero.combat_menu(goblin2)
        goblin2.attack(hero)
    print("two kills? That it your getting mike")
    print("ROUND 2\n")
    goblin3 = goblin("Mike", "Big", 30, 30)
    while hero.HP > 0 and goblin3.alive:
        hero.combat_menu(goblin3)
        goblin2.attack(hero)
    print("\nHey congrats you did it, you beat the game!")              



## MAIN ##
def main():
    WT_Tutorial() 

     
if __name__ == '__main__':
    main()

# encapsulation and polymorphism in final




## TEST ##

# hero = player(15, 15, "bob", [])
        
# hero.inventory()
# print("I will add 42 coins to players inventory")
# hero.looting([42, "coins"])
# hero.inventory()
# print("I will add one book and an addition 8 coins")
# hero.looting([8, "coins"])
# hero.looting([1, "book"])
# hero.inventory()