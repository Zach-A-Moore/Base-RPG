from Basic_Functions import yesno_loop, choice_num_loop, print_choice, menu_handler
from Basic_Objects import Scene, Object, Player, Tracker, Goblin, Dialogue_Tree, Dialogue_Node, load_player, save_player
from Consumables import consumable_tracker
import json
import ast

file_path = r"C:\Users\zacha\OneDrive\Desktop\mooreHON\V2.0 text files\hero_save.txt"

hero = load_player(file_path)


print(hero.data.get("CHEESE"))
# print(hero)

#### Dialogue Tree ####

### Goblin Dialogue ###

D_1_1_txt = ("Well my family the O'riels have been here for generations.\n",\
             "I don't know much about him, but he is a good boss.\n")

D_1_1 = Dialogue_Node("D_1_1", "How do you know the wizard?", "The wizard is upstairs, but I don't know him well.\n")

D_1_txt = ("The goblin look up at you, 'Well, I'm Tute!, I guard the tower stranger.'\n",\
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
    WT_scrap = Scene(["Drawings", "Books", "Spittoon", "Exit"])

    while True:
        temp_answer = menu_handler(WT_main_room)

        if (temp_answer == "Scrap"):
            temp_answer = menu_handler(WT_scrap)

            if (temp_answer == "Spittoon"):
                print()
                







def main():
    wizard_tower()

if __name__ == "__main__":
    main()
