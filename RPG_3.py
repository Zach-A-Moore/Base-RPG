from Basic_Functions import yesno_loop, choice_num_loop, print_choice
from RPG_3_class import Scene, Object, Player, Tracker, goblin



# Intro 
temp_name = input("Welcome to Veliam, what is your name? (12 chr limit) ")
hero = Player(30, 30, temp_name[0:16:1], [])
print (f"Well {hero.name} you've found yourself in my tower, take a look around")
answer_explore = yesno_loop(input("Take a look around? Y/N: "),\
                            "Take a look around? Y/N: ")
temp_index = 0
# Would'nt like to look around, will run through the list then print ...
while (answer_explore == 0):
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
    answer_explore = yesno_loop(input("Would you like to leave? Y/N: "),\
                                "Would you like to leave? Y/N: ")
   
print(" A large room lays before you a kindly wizard waiting by the door,",
        " \n a deep black stone is what makes up most of walls and floor.\n",
    "A massive cauldron in the center of the room",
    "bubbles pleasantly, Alongside this a weapons rack\n",
    "which holds a pretty cool looking sword\n")
WT_explore = Scene(["The cauldron", "The weapons rack",
                    "The window","Cheese?"])
WT_trackers = Tracker()
WT_trackers.compile_track(["EXIT", "CHEESE", "S_CAULDRON"])

while answer_explore == 1:
    print(WT_explore)
    temp_input = input("What would you like to choose? ")
    temp_input = choice_num_loop(WT_explore.compile_scene(), temp_input)
    choice = WT_explore.choices[temp_input - 1]

    if choice == "Cheese?" and WT_explore.choices[3] == "Cheese?":
        WT_explore.del_choice("Cheese?")
        hero.loot([1, "CHEESE"])
        print("You have chosen a path you can not return from, may god have mercy",
                " on your soul")
        print("\n You have gained, CHEESE \n")

    if choice == "The window"

