from Basic_Functions import choice_num, choice_num_loop, print_choice
from Consumables import consumable_tracker
import sys
import random 

class Scene:
    """ menu handler """

    def __init__(self, choices : list[str] = []):
        self.choices = choices.copy()


    def __str__ (self) -> None:
        print_choice(self.compile_scene())
        return (" ")

    def compile_scene(self) -> dict[str:int]:
        temp_dict = {}
        tracker = 1
        for elements in self.choices:
            temp_dict[elements] = tracker
            tracker += 1
        return temp_dict
    
    def del_choice(self, key : str):
        tracker = 0
        found = -1
        for element in self.choices:
            if element == key:
                found = tracker
            tracker += 1
        if found != -1:
            del self.choices[found]

    def add_choice(self, key : str):
        """adds a choice to the menu"""
        self.choices.append(key)


class Object:

    def __init__(self, name : str, amount : int):
        self.name = name
        self.amount = amount

    def update(self, amount : int):
        self.amount += amount

    def looted (self):
        temp = self.amount
        self.amount = 0
        return [temp, self.name]
    
class Tracker:

    def __init__(self, trackers : dict[str : int] = {}):
        self.trackers = trackers.copy()

    def compile_track(self, names : list[str], default : int = 0):
        for element in names:
            self.trackers[element] = default

    def update(self, name : str, new : int):
        """new will act as a +="""
        for key, value in self.trackers.items():
            if key == name:
                self.trackers[key] += new

    def get(self, name : str) -> int:
        """returns the value of the key"""
        for key, value in self.trackers.items():
            if key == name:
                return value
        return 404
    
    def set(self, name : str, new : int) -> None:
        """sets the value of the key"""
        for key in self.trackers.keys():
            if key == name:
                self.trackers[key] = new

    def delete(self, name):
        for key in self.trackers.keys():
            if key == name:
                del self.trackers[key]

class Entity:
    def __init__(self, name: str, HP: int, maxHP: int):
        self.name = name
        self.HP = HP
        self.maxHP = maxHP

    def hurt(self, DMG: int, attacker_name: str):
        self.HP -= DMG
        if self.HP <= 0:
            self.HP = 0
            self.on_death(attacker_name)

    def heal(self, amount: int):
        self.HP += amount
        if self.HP > self.maxHP:
            self.HP = self.maxHP

    def on_death(self, attacker_name: str):
        """Override in child classes for death behavior"""
        print(f"{self.name} was killed by {attacker_name}")

class Player(Entity): # declares the class
    def __init__(self, HP : int, maxHP : int, name : str,
                items : list[list[int, str]]=[],
                weapons : list[list[str,int,int,int]]=[]): # ["name", die #, die type, Hit bonus, damage bonus]
        super().__init__(name, HP, maxHP)
        self.items = items
        self.weapons = weapons

    def __str__(self): 
        ## sample text:
        # The Hero Bob
        # HP 20/20
        #
        return f"The Hero {self.name}\nHP {self.HP}\\{self.maxHP}\n"
    
    def on_death(self, attacker_name: str):
        print(f"You were killed by {attacker_name}")
        sys.exit()

    def loot(self, item : list[int, str]):
        name = item[1]
        amount = item[0]
        tracker = 0
        in_inventory = False
        for obj in self.items:
            if obj[1] == name:
                self.items[tracker][0] += amount
                in_inventory = True
            tracker += 1
        if not in_inventory:
            self.items.append([amount, name])

    def loot_weapon(self, weapon : list[str,int,int]) -> None:
        self.weapons.append(weapon)

    def inventory_check(self) -> None:
        if self.items == []:
            print("you have no items")
        else:
            temp = 1
            for element in self.items:
                tracker = ""
                if element[0] > 1:
                    tracker = "\'s"
                print(f"{temp}.) {element[1]:<15}: {element[0]}{tracker}")
                temp += 1
        # 1 : ["name", die #, die type, Hit bonus, damage bonus]
        if self.weapons == []:
            print("you have no weapons")
        else:
            for name,die_num,die_type,hit,dmg in self.weapons:
                print(f"{name:<10}: {die_num}d{die_type} +",
                        f"{dmg} damage with a +{hit} bonus to hit")
        print()
    

    def attack(self, other : Entity):
        print(f"\nWhat weapon would you like to use?")
        temp_tracker = 1
        temp_menu = {}
        for lists in self.weapons:
            temp_menu[lists[0]] = temp_tracker
            temp_tracker += 1
        print_choice(temp_menu)
        temp_input = input("Enter here: ")
        temp_input = choice_num_loop(temp_menu, temp_input)
        current_weapon = self.weapons[temp_input - 1]
        damage = current_weapon[1] * (random.randint(1,current_weapon[2]))\
               + current_weapon[4]
        other.hurt(damage, self.name)
        print(f"You did {damage} damage with {current_weapon[0]}")

    def use_item(self) -> None:
        print("What item would you like to use?")
        temp_tracker = 1
        temp_menu = {}
        for lists in self.items:
            temp_menu[lists[1]] = temp_tracker
            temp_tracker += 1
        if not self.items:
            print("You have no items to use")
            return
        else:
            temp_menu["Exit"] = temp_tracker
        print_choice(temp_menu)
        temp_input = input("Enter here: ")
        temp_input = choice_num_loop(temp_menu, temp_input)
        if temp_input == temp_tracker:
            return
        current_item = self.items[temp_input - 1]
        consumable_tracker(current_item[1], self)
        current_item[0] -= 1
        if current_item[0] == 0:
            self.items.pop(temp_input - 1)


    def combat_menu(self, other):
        temp_tracker = 0
        while True:
            temp_menu = {"Check Stats" : 1, "Check Enemy" : 2, "Attack" : 3,\
                         "Use Item" : 4}
            print("What would you like to do?")
            print_choice(temp_menu)
            temp_input = input("Enter here: ")
            temp_input = choice_num_loop(temp_menu, temp_input)
            if temp_input == 1:
                input(f"{self}")
            if temp_input == 2:
                input(f"{other}")
            if temp_input == 3:
                self.attack(other)
                break
            if temp_input == 4:
                self.use_item()

class Goblin(Entity):
    """ Goblin class, inherits from Entity """
    def __init__(self, name: str = "Wretch", weapon: str = "Small",
                 maxHP: int = 15, HP: int = 15, alive: bool = True):
        super().__init__(name, HP, maxHP)
        self.weapon = weapon
        self.alive = alive

    def __str__(self):
        if (self.HP / self.maxHP) > .5:
            status = "Healthy"
        elif (self.HP / self.maxHP) > .3:
            status = "Injured"
        elif (self.HP / self.maxHP) > 0:
            status = "Critically Injured"
        else:
            status = "Dead"
        
        return f"The goblin {self.name} has a {self.weapon} weapon\n HP {self.HP}/{self.maxHP}\n Status: {status}"
    
    def damage(self) -> None:
        if self.weapon == "Big":
            return (random.randint(1,10) + 4)
        elif self.weapon == "Medium":
            return (random.randint(1,6) + 2)
        else:
            return (random.randint(1,4))

    def attack(self, other : Entity) -> None:
        amount = self.damage()
        other.hurt(amount, self.name)
        print(f"The goblin did {amount} damage")


    def set_name(self, name : str) -> None:
        "updates name"
        self.name = name

    def get_name(self) -> None:
        "print name"
        return self.name
    
    def get_health(self) -> None:
        "print current health out of max health"
        return f"{self.HP}/{self.maxHP}"

def Goblin_generator() -> Goblin:
    """Generates a goblin with random stats"""
    name = random.choice(["Wretch", "Grunt", "Snatcher", "Stabber"])
    weapon = random.choice(["Small", "Medium"])
    maxHP = random.randint(10, 20)
    HP = maxHP
    return Goblin(name, weapon, maxHP, HP)

def tester():
    menu = Scene(["window", "wall", "exit"])
    assert menu.compile_scene() == {"window" : 1, "wall" : 2, "exit" : 3}

    menu.del_choice("window")
    assert menu.compile_scene() == {"wall" : 1, "exit" : 2}

testing = 0
def main():
    if testing:
        tester()

if __name__ == '__main__':
    main()