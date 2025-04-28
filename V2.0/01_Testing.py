from Basic_Functions import yesno_loop, choice_num_loop, print_choice, menu_handler
from Basic_Objects import Scene, Object, Player, Tracker, Entity, Goblin
from Consumables import consumable_tracker
from unittest.mock import patch

# this should be a universal test for all or most functions from the codebase
# beyond basic testing use "with patch", to automaticcaly put an input in the
# input function, so you can test the code without having to manually input

def test_consumable():
    bob = Player(25, 30, "Bob", [])
    print(bob)
    consumable_tracker("CHEESE", bob)
    print(bob)
    assert bob.maxHP == 35
    assert bob.HP == 30
    consumable_tracker("SMALL HEALTH POTION", bob)
    print(bob)
    assert bob.HP == 35

def test_Inventory_consumables():
    bob = Player(10, 100, "Bob", [])
    bob.loot([2, "SMALL HEALTH POTION"])
    with patch('builtins.input', side_effect=['1', '1']):
        bob.use_item()
        bob.use_item()
    assert bob.HP == 30
    bob.loot([10, "CHEESE"])
    bob.loot([1, "SMALL HEALTH POTION"])
    bob.loot([1, "?????"])
    with patch('builtins.input', side_effect=['3']):
        bob.use_item()
    print(bob.inventory_check())

def test_Inventory_weapons():
    # ["name", die #, die type, Hit bonus, damage bonus]
    # weapon[0] = name of weapon
    # weapon[1] = die number, how many dice to roll, the 3 in 3d6
    # weapon[2] = die type, what type of die to roll, basically the range of damage
    # weapon[3] = hit bonus, how much to add to the roll, not yet implemented
    # weapon[4] = damage bonus, how much to add to the damage roll
    bob = Player(10, 100, "Bob", [])
    dummy = Entity("dummy", 100, 100)
    bob.loot_weapon(["Sword", 2, 6, -1, 4]) # 2d6+4
    bob.attack(dummy)



def main():
    # test_consumable()
    # test_Inventory_consumables()
    test_Inventory_weapons()
    print("All tests passed")

if __name__ == "__main__":
    main()