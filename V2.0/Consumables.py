from Basic_Objects import Scene, Object, Player, Tracker, Goblin, Entity
import random

def consumable_tracker(name : str, creature : Entity) -> None:
    clean = name.strip()
    clean = clean.upper()
    if (name == "SMALL HEALTH POTION"):
        small_hp(creature)
        


def small_hp(creature : Entity):
    creature.heal(5)