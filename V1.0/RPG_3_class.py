from Basic_Functions import choice_num, choice_num_loop, print_choice
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
        """new will act as a ="""
        for key, value in self.trackers.items():
            if key == name:
                self.trackers[key] = new

    def delete(self, name):
        for key in self.trackers.keys():
            if key == name:
                del self.trackers[key]

class Player: # declares the class
    def __init__(self, HP : int, maxHP : int, name : str, items : list[list[int, str]]=[],\
                 weapons : list[list[str,int,int,int]]=[]):
        self.HP = HP
        self.maxHP = maxHP
        self.name = name
        self.items = items
        self.weapons = weapons

    def __str__(self): 
        ## sample text:
        # The Hero Bob
        # HP 20/20
        #
        return f"The Hero {self.name}\nHP {self.HP}\\{self.maxHP}\n"
    
    def hurt(self, DMG : int, name : str) -> None:
        self.HP -= DMG
        if (self.HP <= 0):
            print(f"you were killed by {name}")
            sys.exit()

    def heal(self, num : int) -> None:
        self.HP += num
        if self.HP > self.maxHP:
            self.HP = self.maxHP

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

    def inventory(self) -> None:
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
    

    def attack(self, other : Object):
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
               + current_weapon[3]
        other.hurt(damage, self.name)

    def use_item(self) -> None:
        temp_menu_1 = {}
        temp_tracker = 1
        temp_tracker_items = 0
        temp_tracker_list = []
        temp_input = ""
        temp_solution = "" # need to rewrite object class and read from it
        for items in self.items:
            if items[0] <= 0:
                temp_tracker_items += 1
                continue
            else:
                temp_menu_1[items[1]] = temp_tracker
                temp_tracker_list.append(temp_tracker_items)
                temp_tracker += 1
                temp_tracker_items += 1
            if temp_menu_1 == []:
                print("You dont have any items left")
                break
            else:
                for num in temp_tracker_list:
                    self.items[num][0] -= 1
                print_choice(temp_menu_1)
                temp_input = input("Enter here: ")
                temp_input = choice_num_loop(temp_menu_1, temp_input)
                for key, value in temp_menu_1.items():
                    if value == temp_input:
                        print(f"You use a {key}")
                        temp_solution = key
                        break
                if temp_solution == "POTION":
                    self.heal(10)
                if temp_solution == "MOON CHEESE":
                    self.maxHP += 10


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
            for lists in self.items:
                if not lists[0] <= 0:
                    temp_tracker = 1
            if temp_input == 4:
                if self.items or temp_tracker == 0:
                    print("You have no items to use")
                else:
                    self.use_item()

class goblin:
    """ this class is meant to define a goblin object, which takes a name as a 
    str, a weapon as a str classified by small, medium, and big, maxHp and HP
    which mirror the player class, that being keeping track of health and it's 
    limit, and an alive stat that determines if health has reached
    damage determined by the goblins weapon will generate a random number
    hurt takes a name and int to effect the goblins HP, if it reaches zero
    the goblins alive stat will change to false and print a message, 
    otherwise a message will print displaying the damage taken and change
    of the goblin HP.
    attack takes a player class, and using damage will subtract a number
    from the players HP, and possibly kill them with a message accordingly.
    """
    def __init__ (self, name : str="Wretch", weapon : str="Small",\
                  maxHP : int=15, HP : int=15, alive : bool=True):
        self.weapon = weapon
        self.maxHP = maxHP
        self.HP = HP
        self.name = name
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
        
        return f"The goblin {self.name} has a {self.weapon}\
                 weapon\n HP {self.HP}/{self.maxHP}\n Status: {status}"
    
    def damage(self) -> None:
        if self.weapon == "Big":
            return (random.randint(1,10) + 4)
        elif self.weapon == "Medium":
            return (random.randint(1,6) + 2)
        else:
            return (random.randint(1,4))
        
    def hurt(self, dmg : int, name: str) -> str:
        if self.HP <= dmg:
            self.HP = 0
            self.alive = False
            print(f"Goblin {self.name} was killed by {name}\n")
        else:
            self.HP -= dmg
            print(f"Goblin {self.name} has taken {dmg}\n")

    def attack(self, other) -> None:
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



def tester():
    menu = Scene(["window", "wall", "exit"])
    assert menu.compile() == {"window" : 1, "wall" : 2, "exit" : 3}

    menu.del_value("window")
    assert menu.compile() == {"wall" : 1, "exit" : 2}

testing = False
def main():
    if testing:
        tester()

if __name__ == '__main__':
    main()