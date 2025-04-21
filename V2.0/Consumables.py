
def consumable_tracker(name : str, creature : object) -> None:
    clean = name.strip()
    clean = clean.upper()
    if (name == "SMALL HEALTH POTION"):
        small_hp(creature)
        


def small_hp(creature : object):
    creature.heal(5)