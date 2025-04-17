from Basic_Functions import yesno_loop, choice_num_loop, print_choice
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

