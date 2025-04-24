from Basic_Functions import yesno_loop, choice_num_loop, print_choice, menu_handler
from Basic_Objects import Scene, Object, Player, Tracker, Goblin, Dialogue_Tree, Dialogue_Node
from Consumables import consumable_tracker
import ast

file_path = r"C:\Users\zacha\OneDrive\Desktop\mooreHON\V2.0 text files\hero_save.txt"

with open(file_path, "r") as file:
    line = file.readline()
    parts = line.strip().split(',', 4)  # split only the first 4 commas

    hero_name = parts[0].strip()
    hero_HP = int(parts[1].strip())
    hero_maxHP = int(parts[2].strip())

    # Use ast.literal_eval for safe evaluation of list strings
    hero_items = ast.literal_eval(parts[3].strip())
    hero_weapons = ast.literal_eval(parts[4].strip())

hero = Player(hero_HP, hero_maxHP, hero_name, hero_items, hero_weapons)

#### Dialogue Tree ####

### Goblin Dialogue ###

D_1_1_txt = ("Well my family the O'riels have been here for generations.\n"+
             "I don't know much about him, but he is a good boss.\n")

D_1_1 = Dialogue_Node("D_1_1", "How do you know the wizard?", "The wizard is upstairs, but I don't know him well.\n")

D_1_txt = ("The goblin look up at you, 'Well, I'm Tute!, I guard the tower stranger.'\n",+
          "for the wizard is upstairs'\n")
D_1 = Dialogue_Node("D_1", "What are you doing here?", D_1_txt, children=[D_1_1] )


def wizard_tower():
    print("You descend the stone stairs, each foot step echoing in the hallow tower\n"+
          "you reach the first floor, a large circular room, a chest to the right and a goblin\n"+
          "standing by the main door. It nods as you walk in. A window and some scrap adorn the walls\n")
    ### main room
    WT_main_room = Scene(["Goblin", "Chest", "Window", "Scrap"])
    ## goblin
    WT_goblin = Scene(["Talk", "Give", "Attack", "Exit"])
    # goblin talk
    WT_goblin_talk = Scene(["'What are you doing here?'", "'Do you know the Wizard upstairs?'",
                            "'What's your name?'", "'What's in the chest?'"])
    WT_goblin_give = Scene(["Give Cheese", "Give Potion", "Give Sword", "Exit"])
    ## chest
    WT_chest = Scene(["Open", "Exit"])
    ## window
    WT_window = Scene(["Look", "Exit"])
    ## scrap
    WT_scrap = Scene(["Drawings", "Books", "Suspicious Tin", "Exit"])
