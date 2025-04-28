from Basic_Functions import choice_num, choice_num_loop, print_choice, menu_handler
from Consumables import consumable_tracker
import sys
import random 
import ast
import csv

class Scene:
    """ menu handler, used as a fancy list. makes menu handling more efficient"""

    def __init__(self, choices : list[str] = []):
        self.choices = choices.copy()


    def __str__ (self) -> None:
        """ prints the menu in a readable format
        1.) choice 1
        2.) choice 2
        3.) choice 3"""

        print_choice(self.compile_scene())
        return (" ")

    def compile_scene(self) -> dict[str:int]:
        temp_dict = {}
        tracker = 1
        for elements in self.choices:
            temp_dict[elements] = tracker
            tracker += 1
            # print(f"Debug: choices={self.choices}, compiled={temp_dict}")
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
    """Object class, used for items and weapons"""

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
    """Tracker class, used for tracking stats and other things in scenes to
    increase interactivity"""

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
    def __init__(self, name: str, HP: int, maxHP: int,
                 data : Tracker = Tracker()):
        self.name = name
        self.HP = HP
        self.maxHP = maxHP
        self.data = data

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
    def __init__(self, HP : int, maxHP : int, name : str, data : dict[str : int]={},
                items : list[list[int, str]]=[],
                weapons : list[list[str,int,int,int]]=[], # ["name", die #, die type, Hit bonus, damage bonus]
                XP : int=0, skills : dict[str : int]={}): 
        super().__init__(name, HP, maxHP, data)
        self.items = items
        self.weapons = weapons
        self.XP = XP
        self.skills = skills
        self.data = data

    def __str__(self): 
        output = f"\nThe Hero {self.name}\n"
        output += f"HP {self.HP}/{self.maxHP}       XP {self.XP}\n\n"
        # Skills
        output += "Skills:\n"
        if self.skills:
            for skill, level in self.skills.items():
                output += f"        {skill} / {level}\n"
        else:
            output += "        None (loser)\n"
        # Items
        output += "Items:\n"
        if self.items:
            for amount, name in self.items:
                output += f"        {name} / {amount}\n"
        else:
            output += "        None\n"
        # Weapons
        output += "Weapons:\n"
        if self.weapons:
            for name, die_num, die_type, hit_bonus, dmg_bonus in self.weapons:
                output += f"        {name} / {die_num}d{die_type} + {dmg_bonus}\n"
        else:
            output += "        None\n"
        return output
    
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

def save_player(player: Player, filepath: str, data: dict[str : int] = None):
    with open(filepath, mode="w", newline='') as file:
        fieldnames = ["name", "HP", "maxHP", "XP", "skills", "items", "weapons", "data"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        writer.writerow({
            "name": player.name,
            "HP": player.HP,
            "maxHP": player.maxHP,
            "XP": player.XP,
            "skills": str(player.skills),
            "items": str(player.items),
            "weapons": str(player.weapons),
            "data": str(player.data)
        })

def load_player(filepath: str) -> Player:
    with open(filepath, mode="r", newline='') as file:
        reader = csv.DictReader(file)
        row = next(reader)

        name = row["name"]
        HP = int(row["HP"])
        maxHP = int(row["maxHP"])
        XP = int(row["XP"])
        skills = ast.literal_eval(row["skills"])
        items = ast.literal_eval(row["items"])
        weapons = ast.literal_eval(row["weapons"])
        data = ast.literal_eval(row["data"])

        
        player = Player(HP, maxHP, name, data, items, weapons, XP, skills)

        return player

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

class Dialogue_Tree:
    def __init__(self, name: str, options: list["Dialogue_Node"] = []):
        self.name = name
        self.options = options
    
    def add_option(self, nodes: list["Dialogue_Node"]) -> None:
        """Adds a list of nodes to the tree"""
        for node in nodes:
            self.options.append(node)

    def remove_option(self, node: "Dialogue_Node") -> None:
        """Removes a node from the tree"""
        if node in self.options:
            self.options.remove(node)
        else:
            print(f"Node {node.name} not found in options.")

    def run(self) -> None:
        """Runs the dialogue tree"""
        choices = [node for node in self.options if node.parent is None]
        
        if not choices:
            print("No starting dialogue options available.")
            return
        
        for node in choices:
            if node.visited:
                choices.remove(node)
        
        scene = Scene([])
        while choices:
            scene.choices = []  # Clear previous choices
            for node in choices:
                scene.add_choice(node.text_option)
            choice = menu_handler(scene)
            
            if choice == "exit":
                break
            
            temp_node = None
            for node in choices:
                if node.text_option == choice:
                    temp_node = node
                    break
            
            if temp_node is None:
                print("Invalid choice selected.")
                continue
            
            # Execute the node's function with arguments if provided
            if temp_node.function1:
                temp_node.function1()
            if temp_node.function2:
                temp_node.function2()
            
            print(temp_node.text_response)
            temp_node.visited = True  # Mark node as visited
            choices = temp_node.children  # Move to child nodes
            
            if not choices:
                print("Dialogue ended.")
                break

class Dialogue_Node:
    def __init__(self, name: str, text_option: str, text_response: str,
                 parent: object = None, children: list[object] = [],
                 function1: callable = None,
                 function2: callable = None,
                 visited: bool = False) -> None:
        self.name = name
        self.text_option = text_option
        self.text_response = text_response
        self.parent = parent
        self.children = children
        self.function1 = function1
        self.function2 = function2
        self.visited = visited

    def remove_child(self, node : object) -> None:
        """Removes the node from the tree"""
        if node in self.children:
            self.children.remove(node)
        else:
            print(f"Node {node.name} not found in children.")
    
    def delete(self) -> None:
        """Deletes the node from the tree"""
        if self.parent:
            self.parent.remove_option(self)
        else:
            self.delete()


def dialogue_visited(node: "Dialogue_Node") -> None:
    """Marks the node as visited"""
    node.visited = True

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