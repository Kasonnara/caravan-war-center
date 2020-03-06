"""
This can be modified to represent the full inventory of card that you have: buidings, units, number of copies,
their levels, their stars, theirs equipments, etc.

By defaut the config is set as if all building, units and spells are level 15, equipments level 7 if available
and no stars. Quantities have been set with some common values at this level. (6 legendary, 10 epic+,
1 epic (assuming they are automatically reincarnated), 30 rare, 100 common)

"""

from collections import namedtuple
from typing import Type

from buildings.buildings import Mill, TransportStation, Bank, Storage, Laboratory, Tavern, Camp, Academy, Weaponsmith, \
    Garage, WorkShop, Forge, HeroTemple, Altar
from spells.spells import Ice, Storm, Meteor, Poison, Landmine, Arrow, VehiculeBoost, ModuleBoost, SpeedBoost, \
    AttackSpeedBoost, AttackBoost, LifeBoost
from units.bandits import Demon, Djin, Inferno, VikingLeg, StealerLeg, Chaman, DarkKnightLeg, Mecha, DarkKnight, Lich, \
    Viking, Stealer, Berserk, Spider, Hunter, Brute, Alchimist, Maraudeur, Lutin, Drone, Archer, Condor, Momie, LichLeg, \
    MomieLeg, CondorLeg
from units.equipments import Weapon, Armor
from units.guardians import Seraphin, Golem, DemonSlayer, Canonner, Paladin, Hammer, Sparte, Griffon, Marchal, Sword, \
    Jetpack, Shield, Knight, Healer, Guard, Scout, Follet, Wizard, SparteLeg, GriffonLeg, HammerLeg, PaladinLeg, \
    MarchalLeg
from units.heroes import Zora, Dalvir
from units.towers import Sentinelle, Arbalete, Eolance, Sniper, HeavySniper, Mage, Lightning, Stormspire, Fire, Bomber, \
    Canon, Hydra, MissileLaucher, Hospital, Armory, Tambour, Garnison
from units.vehicules import Train, Dirigeable, Helicopter, Wagon, Chariot, Charrette, Speeder, Buggy, WagonLeg, \
    HelicopterLeg, BuggyLeg
from units.weapons import Shotgun, Mortar, Chaingun, Laser, Tesla, FlameTrower, Balista, LaserLeg, ChaingunLeg, \
    FlameTrowerLeg, Barrier

CardStock = namedtuple('CardStock', 'card quantity')
"""A named tuple containing a unit type and the number of copies owned for units of which more than one copy c
an be obtained."""

buildings = {
    Mill(15),
    TransportStation(15),
    Bank(15),
    Storage(15),
    Laboratory(15),
    Tavern(15),
    Camp(15),
    Academy(15),
    Weaponsmith(15),
    Garage(15),
    WorkShop(15),
    Forge(7),
    HeroTemple(5),
    Altar(8),
    }

buildings_dict = {
    type(building).__name__: building
    for building in buildings
    }

guardians = {
    CardStock(Seraphin(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 6),
    CardStock(Wizard(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 6),
    CardStock(Golem(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 6),
    CardStock(Canonner(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 6),
    CardStock(SparteLeg(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 10),
    CardStock(GriffonLeg(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 10),
    CardStock(DemonSlayer(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 6),
    CardStock(HammerLeg(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 10),
    CardStock(PaladinLeg(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 10),
    CardStock(MarchalLeg(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 10),

    CardStock(Griffon(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 1),
    CardStock(Sparte(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 1),
    CardStock(Paladin(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 1),
    CardStock(Marchal(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 1),
    CardStock(Hammer(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 1),

    CardStock(Knight(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 30),
    CardStock(Shield(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 30),
    CardStock(Jetpack(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 30),
    CardStock(Sword(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 30),
    CardStock(Healer(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 30),

    CardStock(Guard(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 100),
    CardStock(Scout(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 100),
    CardStock(Follet(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 100),
    }

bandits = {
    CardStock(Demon(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 6),
    CardStock(Djin(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 6),
    CardStock(Inferno(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 6),
    CardStock(Chaman(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 6),
    CardStock(MomieLeg(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 10),
    CardStock(VikingLeg(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 10),
    CardStock(StealerLeg(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 10),
    CardStock(LichLeg(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 10),
    CardStock(DarkKnightLeg(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 10),
    CardStock(Mecha(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 6),
    CardStock(CondorLeg(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 10),

    CardStock(Condor(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 1),
    CardStock(DarkKnight(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 1),
    CardStock(Momie(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 1),
    CardStock(Viking(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 1),
    CardStock(Lich(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 1),
    CardStock(Stealer(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 1),

    CardStock(Berserk(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 30),
    CardStock(Spider(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 30),
    CardStock(Hunter(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 30),
    CardStock(Brute(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 30),
    CardStock(Alchimist(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 30),
    CardStock(Lutin(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 30),

    CardStock(Maraudeur(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 100),
    CardStock(Archer(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 100),
    CardStock(Drone(15, stars=0, weapon_item=Weapon(7), armor_item=Armor(7)), 100),
    }

vehicules = {
    CardStock(Train(15, stars=0, armor_item=Armor(7)), 6),
    CardStock(Dirigeable(15, stars=0, armor_item=Armor(7)), 6),
    CardStock(Helicopter(15, stars=0, armor_item=Armor(7)), 1),
    CardStock(Wagon(15, stars=0, armor_item=Armor(7)), 1),
    CardStock(Charrette(15, stars=0, armor_item=Armor(7)), 100),
    CardStock(Chariot(15, stars=0, armor_item=Armor(7)), 30),
    CardStock(Speeder(15, stars=0, armor_item=Armor(7)), 6),
    CardStock(Buggy(15, stars=0, armor_item=Armor(7)), 1),
    CardStock(WagonLeg(15, stars=0, armor_item=Armor(7)), 10),
    CardStock(HelicopterLeg(15, stars=0, armor_item=Armor(7)), 10),
    CardStock(BuggyLeg(15, stars=0, armor_item=Armor(7)), 10),
}

modules = {
    CardStock(Tesla(15, stars=0), 6),
    CardStock(Barrier(15, stars=0), 6),
    CardStock(Laser(15, stars=0), 1),
    CardStock(LaserLeg(15, stars=0), 10),
    CardStock(Chaingun(15, stars=0), 1),
    CardStock(ChaingunLeg(15, stars=0), 10),
    CardStock(FlameTrower(15, stars=0), 1),
    CardStock(FlameTrowerLeg(15, stars=0), 10),
    CardStock(Mortar(15, stars=0), 30),
    CardStock(Shotgun(15, stars=0), 30),
    CardStock(Balista(15, stars=0), 100),
    }

spells = {
    Ice(15),
    Storm(15),
    Meteor(15),
    Poison(15),
    Landmine(15),
    Arrow(15),
    }

convoy_boosts = {
    VehiculeBoost(15),
    ModuleBoost(15),
    SpeedBoost(15),
    AttackSpeedBoost(15),
    AttackBoost(15),
    LifeBoost(15),
    }

heroes = {
    Zora(50, 5, 5, 5, 5, 5),
    Dalvir(50, 5, 5, 5, 5, 5),
    }

ARROW_TOWER_STARS = 0
MAGE_TOWER_STARS = 0
CANON_TOWER_STARS = 0
SUPPORT_TOWER_STARS = 0

towers = {
    Sentinelle(15, stars=ARROW_TOWER_STARS),
    Arbalete(15, stars=ARROW_TOWER_STARS),
    Eolance(15, stars=ARROW_TOWER_STARS),
    Sniper(15, stars=ARROW_TOWER_STARS),
    HeavySniper(15, stars=ARROW_TOWER_STARS),

    Mage(15, stars=MAGE_TOWER_STARS),
    Lightning(15, stars=MAGE_TOWER_STARS),
    Stormspire(15, stars=MAGE_TOWER_STARS),
    Fire(15, stars=MAGE_TOWER_STARS),

    Bomber(15, stars=CANON_TOWER_STARS),
    Canon(15, stars=CANON_TOWER_STARS),
    Hydra(15, stars=CANON_TOWER_STARS),
    MissileLaucher(15, stars=CANON_TOWER_STARS),

    Hospital(15, stars=SUPPORT_TOWER_STARS),
    Armory(15, stars=SUPPORT_TOWER_STARS),
    Tambour(15, stars=SUPPORT_TOWER_STARS),
    Garnison(15, stars=SUPPORT_TOWER_STARS),
    }

MY_CARDS = {
        'Guardians': guardians,
        "Bandits": bandits,
        "Vehicules": vehicules,
        "Modules": modules,
        "spells": spells,
        "Convoy Boosts": convoy_boosts,
        "Heroes": heroes,
        'Buildings': buildings,
        'Towers': towers,
    }
"""Just a dictionary to access stocks of this module using category strings"""