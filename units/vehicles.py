#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    This is a personal project to understand and improve my knowledge/tactics in the game Caravan War.
    Copyright (C) 2019  Kasonnara <kasonnara@laposte.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from typing import List

from common.card_categories import VEHICLES
from common.rarity import Rarity
from units.base_units import MovableUnit, BaseUnit, reincarnation
from common.target_types import TargetType


class Vehicle(MovableUnit):
    move_speed = 1.2
    weapon_slot = 1


class Charrette(Vehicle):
    hp_base = 2280
    shooted_as = TargetType.GROUND
    armor = 3
    cost = 8
    rarity = Rarity.Common


class Chariot(Vehicle):
    hp_base = 1710
    shooted_as = TargetType.GROUND
    armor = 3
    cost = 8
    move_speed = 1.8
    rarity = Rarity.Rare


class Dirigeable(Vehicle):
    hp_base = 3705
    shooted_as = TargetType.AIR
    armor = 3
    cost = 6
    effect_range = 7
    rarity = Rarity.Legendary


class Speeder(Vehicle):
    hp_base = 3800
    shooted_as = TargetType.AIR
    armor = 5
    cost = 8
    effect_range = 4  # Fixme verify value
    effect_speed_boost = 1.3
    rarity = Rarity.Legendary


class Train(Vehicle):
    hp_base = 4251
    shooted_as = TargetType.GROUND
    armor = 8
    cost = 10
    weapon_slot = 2
    rarity = Rarity.Legendary

    def hp_score(self, *args, **kwargs):
        return (
            super().hp_score(*args, **kwargs)
            * 2.5  # Multiply hp_score by 2 (maybe by 3) because the train reflect 50% of the damage taken
            )


class Helicopter(Vehicle):
    hp_base = 2444
    shooted_as = TargetType.AIR
    armor = 0
    cost = 6
    rarity = Rarity.Epic


@reincarnation
class HelicopterLeg(Helicopter):
    pass


class Wagon(Vehicle):
    hp_base = 3250
    shooted_as = TargetType.GROUND
    armor = 5
    cost = 8  # TODO check cost
    rarity = Rarity.Epic


@reincarnation
class WagonLeg(Wagon):
    pass


class Buggy(Vehicle):
    hp_base = 3000
    move_speed = 1.8
    armor = 4
    rarity = Rarity.Epic
    cost = 6
    # TODO spell


@reincarnation
class BuggyLeg(Buggy):
    pass


# Register all defined cards in CARD_DICTIONNARY
VEHICLES.register_cards_in_module(Vehicle, __name__)