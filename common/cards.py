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
from collections import namedtuple, defaultdict
from typing import List, Type, Dict, Set

from common.rarity import Rarity
from common.resources import ResourcePacket
from utils.class_property import classproperty

Upgrade = namedtuple('Upgrade', 'costs requirements')

MAX_LEVEL = 30


class Upgradable:
    upgrade_costs: List[ResourcePacket] = []
    # FIXME: fill <get_upgrade> for all unit and all level, or find an approximation formula
    #        to predict it (cf economy/analyse_costs.py)
    base_building: 'Type[Building]' = None
    base_building_level = 1
    # FIXME; currently cost and requirement doest include the unlock step (frome None to level 1) because it's often
    #   free. But it's not always the case (hero for example), so it may be a good idea to change this.

    # Following parameter will be later defined for category base classes by the register_card_in_module call
    category: str = None

    def __init__(self, level=1):
        assert 0 < level <= MAX_LEVEL, "Level should be in range [1;{}], {} is forbidden".format(MAX_LEVEL, level)
        self.level = level

    def get_upgrade(self):
        """
        Return an Upgrade named tuple containing the costs and requirement for upgrading from (level-1) to (level)
        :param level: int, to level to upgrade to
        :return: named tuple Upgrade{goods_cost: int, gold_cost: int, requirements: List[Upgradable]}
        """
        # Note: for the attribute upgrade_costs (and upgrade_requirements in the case of the HQ) as long as I don't find
        #       a formula to automatically define them at any level, and thus as long as I have to hardcode them, I took
        #       the option of storing them directly in their final form (ResourcePacket instances or Building instances)
        #       this may lead to little more memory usage at the benefit of not having to recreate them at each usage.
        #       Either way I think this is inconsequential, but if in the future we experiment memory problem it can
        #       still be changed.

        assert self.level > 0, "level should be a strictly positive integer"
        assert self.level <= len(self.upgrade_costs), "{} upgrade_costs attribute is not implemented for level {}".format(type(self).__name__, self.level)

        # Note: this function apply to any upgradable item, except the HeadQuarters that re-implement the function.

        if self.level == 1:
            return Upgrade(                                                 # for the first level we only need
                ResourcePacket(),                                               # - it's free # FIXME: not always true
                [self.base_building(self.base_building_level)])                 # - the base building to exist

        return Upgrade(                                                     # for next levels, we need:
            self.upgrade_costs[self.level - 1],                                 #  - paying gold and goods costs
            [type(self)(self.level - 1),                                        #  - previous level
             self.base_building(self.level - 1 + self.base_building_level)])    #  - the base building of the same level


class Card(Upgradable):
    rarity: Rarity = None

    def __init__(self, level=1):
        super().__init__(level)
        self._repr = None

    @classproperty
    def gem_cost(cls):
        return cls.rarity.gem_cost

    @classmethod
    def gold_cost(cls, ligue: 'Ligue'):
        return cls.rarity.gold_cost(ligue)
