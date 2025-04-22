from Basic_Functions import yesno_loop, choice_num_loop, print_choice, menu_handler
from Basic_Objects import Scene, Object, Player, Tracker, Goblin
from Consumables import consumable_tracker

print ("hello world\nYou hear the wizard utter as he casts aside the drapes of," \
" his towers window.\nOpen your eyes and behold the world of Veliam.\n")
temp_name = input("Welcome, what is your name traveler? (12 chr limit) ")

hero = Player(30, 30, temp_name[0:16:1], [])

print (f"Well {hero.name} you've found yourself in my tower, take a look around")
answer_explore = yesno_loop(input("Take a look around? Y/N: "),\
                            "Take a look around? Y/N: ")

temp_index = 0
while (answer_explore == 0): # if the player doesn't want to look around
    wizard_list = ["To spite the wizard you close your eyes\n",
                    "You hear disturbed wizard mumbles\n",
                    "You're really showing it to the man huh\n",
                        "You and the wizard, wait... in silence\n",
                    "...\n", "...\n", "...\n",
                        "you feel the floor beneath your feet\n",
                        "It's a cold floor\n",
                    "...\n", "yep. cold floor\n", "something feels wrong\n",
                        "A deep low disturbance grows in your chest\n",
                    "You Burp\n", "...\n", "Taste's like...\nchicken?\n"]
    if (temp_index < (len(wizard_list) - 1)): # will print until the list is empty
        print(wizard_list[temp_index])
    elif (temp_index == (len(wizard_list) - 1)):
        print(wizard_list[temp_index])
        hero.maxHP += 5
        hero.HP += 5
    else: # if the list is empty, will print "..." forever
        print("...")
    temp_index += 1
    answer_explore = yesno_loop(input("Would you like to open your eyes? Y/N: "),\
                                "Would you like to open your eyes? Y/N: ")

print(" A large room lays before you a kindly wizard waiting by the door,",
        " \na deep black stone is what makes up most of walls and floor.\n",
    "A massive cauldron in the center of the room",
    "bubbles pleasantly, Alongside this a weapons rack\n",
    "which holds a pretty cool looking sword\n")

### main menu
WT_explore = Scene(["The cauldron", "The weapons rack",
                    "The window","Cheese?"])
### window menu
WT_window = Scene(["something interesting", "something valuable",
                   "something else (exit)"])
## window menu - goblin menu
WT_window_goblin = Scene(["Push a brick over", "Let the green man be"])
WT_trackers = Tracker()
WT_trackers.compile_track(["CHEESE", "CAULDRON", "CAULDRON_HP", "WR", "WR_LEFT", "EXIT"])
### weapons rack menu
WT_wp_menu = Scene(["Sword", "Knife", "Mace", "Exit"])
WT_weapons_description = {"Knife" : "A rusty knife lays on the floor",
                          "Sword" : "A silver sword catches your eye, its held by the hilt",
                          "Mace" : "A large mace rest against the rack"}
WT_weapons_stats = {"Knife" : ["Knife", 1, 4, -1, 0],
                    "Sword" : ["Sword", 2, 6, -1, 4],
                    "Mace" : ["Mace", 1, 8, -1, 2]}

while answer_explore == 1: 
    choice = menu_handler(WT_explore)
    # print(WT_explore)
    # temp_input = input("What would you like to choose? ")
    # temp_input = choice_num_loop(WT_explore.compile_scene(), temp_input)
    # choice = WT_explore.choices[temp_input - 1]
    if choice == "Cheese?":
        WT_explore.del_choice("Cheese?")
        WT_trackers.update("CHEESE", 1)
        hero.loot([1, "CHEESE"])
        print("You have chosen a path you can not return from, may god have mercy",
                " on your soul")
        print("\n You have gained, CHEESE \n")
    else:
        WT_explore.del_choice("Cheese?")

    if choice == "The cauldron":
        potion = WT_trackers.get("CAULDRON_HP")
        if WT_trackers.get("CAULDRON") == 0: # first time
            WT_trackers.update("EXIT", 1) # needs a total score of 3 to exit
            WT_trackers.update("CAULDRON", 1)
            print("As you approach the cauldron it vibrant pink solution becomes\n"+
                  "visible, and the pleasant smell of strawberries fills the air\n"+
                  "'Go ahead, grab a bottle', the wizard says\n")
            print("will you take a potion?")
            temp_input = yesno_loop(input("Take a potion? Y/N: "), "Take a potion? Y/N: ")

            if temp_input == 1:
                print("You have taken a potion")
                hero.loot([1, "SMALL HEALTH POTION"])
                hero.inventory_check()
                WT_trackers.update("CAULDRON_HP", 1)
            else:
                print("You walk away from the cauldron, the wizard looks disappointed\n",)

        elif WT_trackers.get("CAULDRON_HP") == 0: # potion not taken
            print("You once again approach the cauldron, have you changed your mind?\n",)
            temp_input = yesno_loop(input("Take a potion? Y/N: "), "Take a potion? Y/N: ")
            if temp_input == 1:
                print("You have taken a potion")
                hero.loot([1, "SMALL HEALTH POTION"])
                hero.inventory_check()
                WT_trackers.update("CAULDRON_HP", 1)
            else:
                print("You walk away from the cauldron, the wizard nods\n",)

        elif WT_trackers.get("CAULDRON_HP") == 1: # potion taken
            print("The smell of strawberries still fills the air, but the cauldron is empty\n",)
            input("return?")

    def take_weapon():
        choice = menu_handler(WT_wp_menu)
        if choice != "Exit":
            hero.loot_weapon(WT_weapons_stats[choice])
            print(f"You have taken the {choice}")
            WT_wp_menu.del_choice(choice)
            WT_trackers.update("WR_LEFT", 1)
            if WT_trackers.get("WR_LEFT") == 3:
                print("~you monster\n")
        else:
            print("You walk away from the weapons rack, the wizard nods\n")

    if choice == "The weapons rack":
        # weapons_left = WT_trackers.get("WR_LEFT")
        #interaction = WT_Trackers.get("WR")
        if WT_trackers.get("WR") == 0: # first time
            print("You walk up to the weapons rack, a large sword catches your eye\n"
                  "A knife lays on the floor, and a large mace rests against the rack\n")
            if yesno_loop(input("Would you like to take a weapon? Y/N: "), "Y/N") == 1:
                WT_trackers.update("WR", 1)
                WT_trackers.update("EXIT", 1)
                take_weapon()
            else:
                input("Indecisive aren't we?")

        elif WT_trackers.get("WR_LEFT") == 1:
            print(f"Oh, no. no yeah you may need another weapon, the {WT_wp_menu.choices[0]} and a {WT_wp_menu.choices[1]}\n"+
                   "lay in front of you")
            if yesno_loop(input("Would you like to take a weapon? Y/N: "), "Y/N") == 1:
                take_weapon()
            else:
                print("Good idea, best not be too greedy\n")

        elif WT_trackers.get("WR_LEFT") == 2:
            print(f"One weapon remains, a {WT_wp_menu.choices[0]}\n"+
                  "You know you don't have to take every weapon right?\n")
            if yesno_loop(input("Would you like to take a weapon? Y/N: "), "Y/N") == 1:
                take_weapon()
            else:
                print("You walk away from the weapons rack, for now...\n")

        elif WT_trackers.get("WR_LEFT") == 3:
            print("You walk toward an empty stand, relishing in your victory\n"+
                  "The wizard looks at you, and shakes his head\n")
            WT_trackers.update("WR_LEFT", 1)
            input("return?")

        else:
            text_list = ["The stand is empty...\n", "Yep, empty stand...\n", "Standing empty\n",
                         "...\n", f"Nothing to see here {hero.name}\n", "Really I mean it\n",
                         "...\n", "...\n", "Okay fine, you win\n",]
            count = WT_trackers.get("WR_LEFT") - 4
            if count < len(text_list):
                print(text_list[count])
            elif WT_trackers.get("WR") == 1:
                hero.loot([1, "NOTHING"])
                print("You have taken NOTHING !!!!")
                WT_trackers.update("WR", 1)
            else:
                print("Yeah sure take another one")
                hero.loot([1, "NOTHING"])
                print("You have taken NOTHING !!!!")
            WT_trackers.update("WR_LEFT", 1)
            input("return?")


    if choice == "The window":
        print("window test")