from Basic_Functions import yesno_loop, choice_num_loop, print_choice, menu_handler
from Basic_Objects import Scene, Object, Player, Tracker, Goblin
from Consumables import consumable_tracker
import random

dummy = Goblin("wretch", "small", 40, 40)
hero = Player(25, 30, "Bob", [])
hero.loot_weapon(["Sword", 2, 6, -1, 4]) # 2d6+4
hero.loot([2, "SMALL HEALTH POTION"])
while dummy.HP > 0:
    hero.combat_menu(dummy)
    dummy.attack(hero)


