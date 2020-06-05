#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This is a personal project to understand and improve my knowledge/tactics in the game Caravan War.
# Copyright (C) 2019  Kasonnara <kasonnara@laposte.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Gains common code
"""
from abc import abstractmethod
from collections import defaultdict
from enum import IntEnum
from typing import List, Dict, Type, Set

from common.cards import MAX_LEVEL
from common.leagues import Rank
from common.resources import ResourcePacket
from common.vip import VIP
from utils.selectable_parameters import UIParameter


class Days(IntEnum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6


# ------------------------ Gains parameters ------------------------
# Used to generate parameter selection UI
rank_param = UIParameter('rank', Rank, display_range=[rank.name for rank in Rank], default_value=Rank.NONE)
vip_param = UIParameter('vip', VIP, display_range=[vip_lvl.name for vip_lvl in VIP],
                        display_txt="VIP", default_value=7)
hq_param = UIParameter('hq_lvl', range(MAX_LEVEL), display_range=[str(vip_lvl + 1) for vip_lvl in range(MAX_LEVEL)],
                       display_txt="HQ", default_value=14)

# You can create new parameters were you think it's the more readable. Here or directly near the Gains classes that
# use them, but just don't forget to add them to the BUDGET_SIMULATION_PARAMETERS for the UI to find them. You can also
# creates new categories if you want just use str keys.

BUDGET_SIMULATION_PARAMETERS = {
    "General": [rank_param, vip_param, hq_param],
    "Traiding": [],
    "Challenges": [],
    "Clan": [],
    "Units": [],
    }
"""Store all UIParameter sorted into categories"""


# ------------------------ Gains abstract class ------------------------
class Gain:
    parameter_dependencies: List[UIParameter] = []

    @classmethod
    @abstractmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, hq_lvl: int = 1, vip: VIP = 1, **kwargs) -> ResourcePacket:
        """Return the resources given for one iteration of the gain"""
        raise NotImplemented()

    @classmethod
    @abstractmethod
    def daily_income(cls, rank: Rank = Rank.NONE, hq_lvl: int = 1, vip: VIP = 1, day: Days = None, **kwargs) -> ResourcePacket:
        """
        Return the daily income from this source.

        :param rank: league.Rank, The rank level of the player
        :param hq_lvl: int, The HeadQuarter level of the player
        :param vip: vip.VIP, The VIP level of the player
        :param day: gains.Days, if defined the function return the gain on this specific day
                                else the function return the average gain per day.
        :param kwargs: optional arguments that may define personal habits (e.g. the usual number of trading launched),(vary on each gain class)
        :return: ResourcePacket
        """
        raise NotImplemented()

    @classmethod
    def weekly_income(cls, rank: Rank = Rank.NONE, hq_lvl: int = 1, vip: VIP = 1, **kwargs) -> ResourcePacket:
        """
        Alias to get daily_income on a whole week

        For the parameters see daily_income
        """
        assert 'day' not in kwargs.keys()
        return cls.daily_income(rank=rank, hq_lvl=hq_lvl, vip=vip, **kwargs) * 7               # More economical
        # return sum(self.daily_income(rank, hq_lvl, vip, day=day, **kwargs) for day in Days)  # Technichally more accurate, but not realy useful yet


# FIXME make a clean and ordered list of gains, and clean categories or even deleting them
GAINS_DICTIONARY: Dict[str, Set[Type[Gain]]] = defaultdict(set)