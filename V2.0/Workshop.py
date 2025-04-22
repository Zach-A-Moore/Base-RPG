def take_weapon_sequence():
    while WT_wp_menu.choices and yesno_loop(input("Would you like to take a weapon? Y/N: "), "Y/N") == 1:
        choice = menu_handler(WT_wp_menu)
        if choice != "Exit":
            hero.loot_weapon(WT_weapons_stats[choice])
            print(f"You have taken the {choice}")
            WT_wp_menu.del_choice(choice)
            WT_trackers.update("WR_LEFT", 1)
            if WT_trackers.get("WR_LEFT") == 3:
                print("~you monster\n")
                break
        else:
            print("You walk away from the weapons rack, the wizard nods\n")
            break
    else:
        if WT_wp_menu.choices:
            print("You walk away from the weapons rack, leaving the clearly inferior weapon behind\n")


if choice == "The weapons rack":
    weapons_left = WT_trackers.get("WR_LEFT")

    if weapons_left == 0:
        print("You walk up to the weapons rack, a large sword catches your eye\n"
              "A knife lays on the floor, and a large mace rests against the rack\n")
        if yesno_loop(input("Would you like to take a weapon? Y/N: "), "Y/N") == 1:
            take_weapon_sequence()
            WT_trackers.update("WR", 1)
        else:
            input("Indecisive aren't we?")

    elif weapons_left == 1:
        print(f"Two weapons remain, a {WT_wp_menu.choices[0]} and a {WT_wp_menu.choices[1]}\n")
        if yesno_loop(input("Would you like to take a weapon? Y/N: "), "Y/N") == 1:
            take_weapon_sequence()
        else:
            print("Good idea, best not be too greedy\n")

    elif weapons_left == 2:
        print(f"One weapon remains, a {WT_wp_menu.choices[0]}\n"
              "You've played this game before, you know the drill\n")
        if yesno_loop(input("Would you like to take a weapon? Y/N: "), "Y/N") == 1:
            take_weapon_sequence()
        else:
            print("You walk away from the weapons rack, feeling merciful today?\n")

    elif weapons_left == 3:
        print("You walk toward an empty stand, relishing in your victory\n"
              "The wizard looks at you, and shakes his head\n")
