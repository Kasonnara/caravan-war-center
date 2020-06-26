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
List gains that obtainable on a daily basis
"""
import itertools
import math
from typing import Optional

from buildings import buildings
from buildings.buildings import Mill, TransportStation
from common.leagues import Rank
from common.rarity import Rarity
from common.resources import ResourcePacket, hero_souls, ResourceQuantity
from common.resources import Resources as R
from common.vip import VIP
from economy.gains.adds import Adds
from economy.gains.abstract_gains import Gain, GAINS_DICTIONARY, rank_param, vip_param, Days
from units.bandits import Bandit
from units.guardians import Guardian
from utils.ui_parameters import UIParameter


class Trading(Gain):
    parameter_dependencies = [rank_param, vip_param]
    duration: int = None
    traiding_limit = None
    goods_cost_multiplier: int = None
    gold_reward_multiplier: float = None

    @classmethod
    def goods_cost(cls, rank: Rank) -> int:
        return - rank.traiding_base * cls.goods_cost_multiplier

    @classmethod
    def gold_reward(cls, rank: Rank, vip: VIP) -> int:
        return rank.traiding_base * cls.gold_reward_multiplier * vip.traiding_profit

    @classmethod
    def daily_max_count(cls, vip: VIP, reset_max_count: float = 0) -> float:
        assert reset_max_count >= 0
        return min(
            24 / (cls.duration * vip.traiding_time),       # Max number of traiding in 24 hours with infinite resets
            cls.traiding_limit * (1 + reset_max_count),    # Max number of traiding according to resets
            )

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, vip: VIP = 1, **kwargs) -> ResourcePacket:
        # TODO add card and reincarnation medals loots
        return ResourcePacket(cls.goods_cost(rank), cls.gold_reward(rank, vip))

    @classmethod
    def daily_income(cls, rank: Rank = Rank.NONE, vip: VIP = 1,
                     daily_trading_count: float = None, **kwargs) -> ResourcePacket:
        max_trading = cls.daily_max_count(vip, reset_max_count=3)
        assert daily_trading_count is None or daily_trading_count < max_trading
        return (
            cls.iteration_income(rank=rank, vip=vip, **kwargs)
            * (max_trading if daily_trading_count is None else daily_trading_count)
            )


daily_10km_trading_count_param = UIParameter(
    'daily_10km_trading_count',
    list(range(30)) + [None],
    display_range=[str(x) for x in range(30)] + ["Max (Auto)"],
    display_txt="10km trading count",
    default_value=None,
    )


class Trading10Km(Trading):
    duration = 0.5
    traiding_limit = 100
    goods_cost_multiplier = 1
    gold_reward_multiplier = 1

    @classmethod
    def daily_income(cls, daily_10km_trading_count: float = None, **kwargs):
        return super().daily_income(daily_trading_count=daily_10km_trading_count, **kwargs)


daily_100km_trading_count_param = UIParameter(
    'daily_100km_trading_count',
    list(range(3 * 5)),
    display_range=[(str(x) if x <= 3 else "{} ({} reset)".format(x, (x-1)//3)) for x in range(3 * 5)],
    display_txt="100km trading count",
    default_value=9,
    )


class Trading100Km(Trading):
    duration = 1
    traiding_limit = 3
    goods_cost_multiplier = 2
    gold_reward_multiplier = 2.6

    @classmethod
    def daily_income(cls, daily_100km_trading_count: float = None, **kwargs):
        return super().daily_income(daily_trading_count=daily_100km_trading_count, **kwargs)


daily_1000km_trading_count_param = UIParameter(
    'daily_1000km_trading_count',
    list(range(2 * 5)),
    display_range=[(str(x) if x <= 2 else "{} ({} reset)".format(x, (x-1)//2)) for x in range(2 * 5)],
    display_txt="1000km trading count",
    default_value=6,
    )


class Trading1000Km(Trading):
    duration = 2
    traiding_limit = 2
    goods_cost_multiplier = 3
    gold_reward_multiplier = 4.8

    @classmethod
    def daily_income(cls, daily_1000km_trading_count: float = None, **kwargs):
        return super().daily_income(daily_trading_count=daily_1000km_trading_count, **kwargs)


daily_best_trading_count_param = UIParameter(
    'daily_best_trading_count',
    list(range(1 * 5)),
    display_range=[(str(x) if x <= 1 else "{} ({} reset)".format(x, x - 1)) for x in range(1 * 5)],
    display_txt="Best trading count",
    default_value=3,
    )


class BestTrading(Trading):
    duration = 4
    traiding_limit = 1
    goods_cost_multiplier = 4
    gold_reward_multiplier = 8

    @classmethod
    def daily_income(cls, daily_best_trading_count: float = None, **kwargs):
        return super().daily_income(daily_trading_count=daily_best_trading_count, **kwargs)


_possible_hero_combinaisons = list(itertools.combinations(hero_souls, 2))
"""List all the possible unordered combinations of 2 hero souls"""

# Declare an additional UI parameter for the lottery gains
selected_heroes_param = UIParameter(
    'selected_heroes',
    _possible_hero_combinaisons,
    display_range=["{}-{}".format(h1.name[:-4], h2.name[:-4]) for h1, h2 in _possible_hero_combinaisons],
    display_txt="Lottery heroes"
    )


class TradingResets(Gain):
    reset_costs = [ResourcePacket(R.Gem(gem_cost)) for gem_cost in (0, -80, -160, -320)]
    cumulative_reset_costs = [ResourcePacket(R.Gem(gem_cost)) for gem_cost in (0, -80, -240, -560)]
    # TODO: factor with other element that implement resets (like the forge)
    # FIXME: make cumulative_reset_costs sums computed from reset_costs

    @classmethod
    def iteration_income(cls, reset_count_same_day: int, vip: VIP = 1) -> ResourcePacket:
        n = max(0, reset_count_same_day - vip.traiding_quota_free_reset)
        # FIXME do not return ResourcePacket, but ResourceQuantity. It's ok but signature must be changed.
        return cls.reset_costs[n]

    @classmethod
    def daily_income(cls,
                     daily_100km_trading_count: float = None,
                     daily_1000km_trading_count: float = None,
                     daily_best_trading_count: float = None,
                     vip: VIP = 1, **kwargs,
                     ) -> ResourcePacket:
        reset_count_same_day = math.ceil(max(
            daily_100km_trading_count / Trading100Km.traiding_limit,
            daily_1000km_trading_count / Trading1000Km.traiding_limit,
            daily_best_trading_count / BestTrading.traiding_limit,
            ))
        n = max(0, reset_count_same_day - vip.traiding_quota_free_reset)
        return cls.cumulative_reset_costs[n]


class Lottery(Gain):
    parameter_dependencies = [rank_param, selected_heroes_param]

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, selected_heroes=_possible_hero_combinaisons[0], **kwargs) -> ResourcePacket:
        return ResourcePacket(
            selected_heroes[0]((30 * 1 + 5 * 4 + 1 * 7) / 100),
            selected_heroes[1]((30 * 1 + 5 * 4 + 1 * 7) / 100),
            R.CapacityToken((3 * 3 + 2 * 4 + 1 * 5) / 100),
            R.Gem((500 * 7 + 250 * 10) / 100),
            R.Goods((rank.traiding_base * 3 * 7 + rank.traiding_base * 1 * 10) / 100),
            R.Gold((rank.traiding_base * 3 * 7 + rank.traiding_base * 1 * 10) / 100),
            )

    @classmethod
    def convert_tickets(cls, ticket_number: int, rank: Rank, selected_heroes=(R.DalvirSoul, R.ZoraSoul), **kwargs) -> ResourcePacket:
        return cls.iteration_income(rank, selected_heroes=selected_heroes, **kwargs) * ticket_number

    @classmethod
    def daily_income(cls, rank: Rank, *args, selected_heroes=(R.DalvirSoul, R.ZoraSoul), **kwargs) -> ResourcePacket:
        return cls.convert_tickets(3, rank, selected_heroes=selected_heroes, **kwargs)


mill_lvl_param = UIParameter(
    'mill_lvl',
    list(range(1, 31)) + [None],
    display_range=[str(lvl) for lvl in range(1, 31)] + ["Auto (= HQ level)"],
    default_value=None,
    )


class MillProduction(Gain):
    @classmethod
    def iteration_income(cls, mill_lvl: Optional[int] = None, hq_lvl=1, vip: VIP = 1, **kwargs) -> ResourcePacket:
        """
        Production per 2 hour
        :param mill_lvl:
        :param hq_lvl:
        :param vip:
        :param kwargs:
        :return:
        """
        return Mill.bihourly_incomes[mill_lvl or hq_lvl] * vip.goods_production

    # TODO daily_collect_count can be miss understood by the user, it would be better to ask it's play hours
    #  (or various play strategy (once a day, twice a day, sparsly all the day, etc.)
    @classmethod
    def daily_income(cls, mill_lvl: Optional[int] = None, hq_lvl=1, vip: VIP = 1, daily_collect_count: int = None,
                     **kwargs) -> ResourcePacket:
        income = cls.iteration_income(mill_lvl=mill_lvl, hq_lvl=hq_lvl, vip=vip, **kwargs) * 12
        if daily_collect_count is not None:
            income = min(income, Mill.storage_limits[mill_lvl or hq_lvl] * daily_collect_count)
        return income


station_lvl_param = UIParameter(
    'station_lvl',
    list(range(1, 31)) + [None],
    display_range=[str(lvl) for lvl in range(1, 31)] + ["Auto (= HQ level)"],
    default_value=None,
    )


class TransportStationProduction(Gain):
    @classmethod
    def iteration_income(cls, station_lvl: Optional[int] = None, hq_lvl=1, vip: VIP = 1, **kwargs) -> ResourcePacket:
        """
        Production per 2 hour
        :param station_lvl:
        :param hq_lvl:
        :param vip:
        :param kwargs:
        :return:
        """
        return TransportStation.bihourly_incomes[station_lvl or hq_lvl] * vip.gold_production

    # TODO daily_collect_count can be miss understood by the user, it would be better to ask it's play hours
    #  (or various play strategy (once a day, twice a day, sparsly all the day, etc.)
    @classmethod
    def daily_income(cls, station_lvl: Optional[int] = None, hq_lvl=1, vip: VIP = 1, daily_collect_count: int = None,
                     **kwargs) -> ResourcePacket:
        # TODO add attack frequency parameter
        income = cls.iteration_income(station_lvl=station_lvl, hq_lvl=hq_lvl, vip=vip, **kwargs) * 12
        if daily_collect_count is not None:
            income = min(income, Mill.storage_limits[station_lvl or hq_lvl] * daily_collect_count)
        return income


class DailyQuest(Gain):

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, **kwargs) -> ResourcePacket:
        # TODO allow partial reward?
        return ResourcePacket(
            R.Goods(2 * rank.traiding_base),
            R.Gold((2 * rank.traiding_base)),
            R.Gem(20),
            R.BeginnerGrowth(100),
            R.LifePotion(1),
            ResourceQuantity((Bandit, Rarity.Rare), 1),
            ResourceQuantity((Guardian, Rarity.Rare), 1),
            )

    @classmethod
    def daily_income(cls, rank: Rank = Rank.NONE, **kwargs) -> ResourcePacket:
        return cls.iteration_income(rank=rank)


class FreeDailyOffer(Gain):

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, **kwargs) -> ResourcePacket:
        return ResourcePacket(R.Goods(rank.traiding_base), R.LifePotion(1))

    @classmethod
    def daily_income(cls, rank: Rank = Rank.NONE, **kwargs) -> ResourcePacket:
        return cls.iteration_income(rank=rank, **kwargs)


ambush_lost_param = UIParameter(
    'ambush_received',
    int,
    display_txt="Defense lost (daily)",
    )

ambush_won_param = UIParameter(
    'ambush_won', 
    int,
    display_txt="Ambush won",
    default_value=20,
    )

temple_lvl_param = UIParameter(
    'temple_lvl',
    list(range(1, 24)) + [None],
    display_range=["{} (HQ {})".format(lvl, lvl + 6) for lvl in range(1, 24)] + ["Auto (= HQ level)"],
    default_value=None,
    )

average_trophy_param = UIParameter(
    'average_trophy',
    [5, 10, 15, 20, 25, 30, 35, 40, 45],
    display_txt="Average trophy",
    default_value=2,
    )


class Ambushes(Gain):
    _ambush_reward = ResourcePacket(
        R.Gem(8),
        R.LifePotion(1/3),
        R.LegendarySoul(1.13),
        R.ReincarnationToken(1.13),
        )
    """Reward average expectation per attack (doesn't take daily limits into account)"""
    _max_reward_per_day = ResourcePacket(
        R.Gem(160),
        R.LifePotion(5),
        R.LegendarySoul(26),
        R.ReincarnationToken(26),
        )

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, temple_lvl=None, hq_lvl=1, average_trophy=15, **kwargs) -> ResourcePacket:
        temple_lvl = temple_lvl or hq_lvl
        return (
            cls._ambush_reward
            + buildings.HeroTemple.ambush_xp_incomes[temple_lvl - 1]  # Assume all ambush are made with a hero in the army
            + R.Goods(rank.traiding_base * 2,5)  # Assume that on average you fight against enemies of the same rank as you, and attack 10km, 100km, 100km and best exchangez indiferently
            + R.Trophy(average_trophy)
        )

    @classmethod
    def daily_income(cls, ambush_won: int = None, rank: Rank = Rank.NONE, temple_lvl=None, hq_lvl=1, average_trophy=15, **kwargs) -> ResourcePacket:
        temple_lvl = temple_lvl or (hq_lvl - 6)
        if ambush_won is None:
            ambush_won = 20
        return ResourcePacket(
            R.Gem(
                min(cls._ambush_reward[R.Gem] * ambush_won,
                    cls._max_reward_per_day[R.Gem])),
            R.LifePotion(
                min(cls._ambush_reward[R.LifePotion] * ambush_won,
                    cls._max_reward_per_day[R.LifePotion])),
            R.LegendarySoul(
                min(cls._ambush_reward[R.LegendarySoul] * ambush_won,
                    cls._max_reward_per_day[R.LegendarySoul])),
            R.ReincarnationToken(
                min(cls._ambush_reward[R.ReincarnationToken] * ambush_won,
                    cls._max_reward_per_day[R.ReincarnationToken])),
            buildings.HeroTemple.ambush_xp_incomes[temple_lvl - 1] * ambush_won,   # Assume all ambush are made with a hero in the army
            R.Goods(rank.traiding_base * 2.5 * ambush_won),  # Assume that on average you fight against enemies of the same rank as you, and attack 10km, 100km, 100km and best exchangez indiferently
            R.Trophy(average_trophy * ambush_won),
            )


ask_for_donation_param = UIParameter(
    'ask_for_donation',
    bool,
    display_txt="Clan Donations",
    default_value=False,
    )


class ClanDonation(Gain):
    donation_bases = [50, 150, 150, 750, 750, 1875, 1875, 3750, 3750, 9000, 9000, 17500, 17500,
                      42500, 42500, 100000, 100000, 255000, 255000, 640000, 640000, 1600000, 1600000,
                      3680000, 3680000, 8160000, 8160000, 16320000, 16320000, 16320000, 16320000]

    @classmethod
    def iteration_income(cls, hq_lvl: int = 1, ask_for_donation: bool = False, **kwargs) -> ResourcePacket:
        if ask_for_donation:
            return ResourcePacket(cls.donation_bases[hq_lvl], cls.donation_bases[hq_lvl])
        else:
            return ResourcePacket()

    @classmethod
    def daily_income(cls, hq_lvl: int = 1, ask_for_donation: bool = False, **kwargs) -> ResourcePacket:
        return cls.iteration_income(hq_lvl=hq_lvl, ask_for_donation=ask_for_donation, **kwargs) * 5


# TODO daily connection reward


GAINS_DICTIONARY['trading'] = {Trading10Km, Trading100Km, Trading1000Km, BestTrading, TradingResets, Ambushes}

GAINS_DICTIONARY['daily'] = GAINS_DICTIONARY['trading'].union(
    {Lottery, MillProduction, TransportStationProduction, Adds, DailyQuest, FreeDailyOffer, ClanDonation})