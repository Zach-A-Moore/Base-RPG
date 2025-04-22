
def consumable_tracker(name : str, creature : object) -> None:
    clean = name.strip()
    clean = clean.upper()
    if (name == "SMALL HEALTH POTION"):
        small_hp(creature)
    elif (name == "CHEESE"):
        cheese(creature)
    else:
        print(f"{name} is not a valid consumable")
        

def small_hp(creature : object):
    creature.heal(10)
    print(f"{creature.name} has healed 10 HP")

def cheese(creature : object):
    creature.maxHP += 5
    creature.HP += 5
    print(f"{creature.name} has used ????")