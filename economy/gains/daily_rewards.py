#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This is a personal project to understand and improve my knowledge/tactics in the game Caravan War.
# Copyright (C) 2019  Kasonnara <wins@kasonnara.fr>
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
import functools
import math
from typing import Optional, Type

from buildings import buildings
from buildings.buildings import Mill, TransportStation
from common.leagues import Rank
from common.rarity import Rarity
from common.resources import ResourcePacket, ResourceQuantity, hero_pair_combinaisons
from common.resources import Resources as R
from common.vip import VIP
from economy.chests import WoodenChest, IronChest, SilverChest, GoldenChest, Chest, RaidChest
from economy.gains.abstract_gains import Gain, rank_param, vip_param, Days, hq_param
from lang.languages import TranslatableString
from units.bandits import Bandit
from units.guardians import Guardian
from utils.ui_parameters import UIParameter


class Trading(Gain):
    parameter_dependencies = [rank_param, vip_param]
    duration: int = None
    traiding_limit: int = None
    goods_cost_multiplier: int = None
    gold_reward_multiplier: float = None
    reward_chest: Type[Chest] = None

    @classmethod
    def goods_cost(cls, rank: Rank) -> int:
        return - rank.traiding_base * cls.goods_cost_multiplier

    @classmethod
    def gold_reward(cls, rank: Rank, vip: VIP) -> int:
        return rank.traiding_base * cls.gold_reward_multiplier * vip.traiding_profit

    @classmethod
    def daily_max_count(cls, vip: VIP, reset_max_count: float = None) -> float:
        assert reset_max_count is None or reset_max_count >= 0
        return min(
            # Max number of traiding in 24 hours with infinite resets
            24 / (cls.duration * vip.traiding_time),
            # Max number of trading with the given number of resets
            cls.traiding_limit * (1 + reset_max_count) if reset_max_count is not None else 100,
            )

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, vip: VIP = 1, **kwargs) -> ResourcePacket:
        # TODO add card and reincarnation medals loots
        return ResourcePacket(cls.goods_cost(rank),
                              cls.gold_reward(rank, vip),
                              ResourceQuantity(cls.reward_chest, 1))

    @classmethod
    def daily_income(cls, rank: Rank = Rank.NONE, vip: VIP = 1,
                     daily_trading_count: float = 0, **kwargs) -> ResourcePacket:
        max_trading = cls.daily_max_count(vip)
        assert daily_trading_count is None or daily_trading_count <= max_trading
        return (
            cls.iteration_income(rank=rank, vip=vip, **kwargs)
            * (max_trading if daily_trading_count is None else daily_trading_count)
            )


daily_10km_trading_count_param = UIParameter(
    'daily_10km_trading_count',
    list(range(30)) + [None],
    display_range=[str(x) for x in range(30)] + ["Max (Auto)"],
    display_txt=TranslatableString("10km trading count", french="Échanges de 10km"),
    default_value=None,
    help_txt=TranslatableString("Select the average number of 10km tradings you sent each day.",
                                french="Sélectionner le nombre moyen d'échange de 10km réalisés par jour."),
    )


class Trading10Km(Trading):
    duration = 0.5
    traiding_limit = 100
    goods_cost_multiplier = 1
    gold_reward_multiplier = 1
    reward_chest = WoodenChest

    @classmethod
    def daily_income(cls, daily_10km_trading_count: float = None, **kwargs):
        return super().daily_income(daily_trading_count=daily_10km_trading_count, **kwargs)

    __display_name = TranslatableString("10km trading", french="Échange de 10km")


def update_tradings_parameter(num_trading_per_reset: int, vip: VIP):
    max_trading_cycle = (1 + vip.traiding_quota_free_reset + 3)
    return (
        list(range(1 + num_trading_per_reset * max_trading_cycle)),
        ['0'] + ["{} {}".format(
            num_reset * num_trading_per_reset + x + 1,
            "" if num_reset == 0 else ("(free reset)" if num_reset <= vip.traiding_quota_free_reset
                                       else "({} reset)".format(num_reset - vip.traiding_quota_free_reset))
            )
         for num_reset in range(max_trading_cycle) for x in range(num_trading_per_reset)]
        )


values_range_100km, dispaly_range_100km = update_tradings_parameter(3, VIP.lvl0)
daily_100km_trading_count_param = UIParameter(
    'daily_100km_trading_count',
    values_range_100km,
    display_range=dispaly_range_100km,
    display_txt=TranslatableString("100km trading count", french="Échanges de 100km"),
    default_value=9,
    update_callback=functools.partial(update_tradings_parameter, 3),
    dependencies=[vip_param],
    help_txt=TranslatableString("Select the average number of 100km tradings you sent each day.",
                                french="Sélectionner le nombre moyen d'échange de 100km réalisés par jour."),
    )


class Trading100Km(Trading):
    duration = 1
    traiding_limit = 3
    goods_cost_multiplier = 2
    gold_reward_multiplier = 2.6
    reward_chest = IronChest

    @classmethod
    def daily_income(cls, daily_100km_trading_count: float = 0, **kwargs):
        return super().daily_income(daily_trading_count=daily_100km_trading_count, **kwargs)

    __display_name = TranslatableString("100km trading", french="Échange de 100km")


values_range_1000km, dispaly_range_1000km = update_tradings_parameter(2, VIP.lvl0)
daily_1000km_trading_count_param = UIParameter(
    'daily_1000km_trading_count',
    values_range_1000km,
    display_range=dispaly_range_1000km,
    display_txt=TranslatableString("1000km trading count", french="Échanges de 1000km"),
    default_value=6,
    update_callback=functools.partial(update_tradings_parameter, 2),
    dependencies=[vip_param],
    help_txt=TranslatableString("Select the average number of 1000km tradings you sent each day.",
                                french="Sélectionner le nombre moyen d'échange de 1000km réalisés par jour."),
    )


class Trading1000Km(Trading):
    duration = 2
    traiding_limit = 2
    goods_cost_multiplier = 3
    gold_reward_multiplier = 4.8
    reward_chest = SilverChest

    @classmethod
    def daily_income(cls, daily_1000km_trading_count: float = 0, **kwargs):
        return super().daily_income(daily_trading_count=daily_1000km_trading_count, **kwargs)

    __display_name = TranslatableString("1000km trading", french="Échange de 1000km")


values_range_best_exchange, dispaly_range_best_exchange = update_tradings_parameter(1, VIP.lvl0)
daily_best_trading_count_param = UIParameter(
    'daily_best_trading_count',
    values_range_best_exchange,
    display_range=dispaly_range_best_exchange,
    display_txt=TranslatableString("Best trading count", french="Meilleurs échanges"),
    default_value=3,
    update_callback=functools.partial(update_tradings_parameter, 1),
    dependencies=[vip_param],
    help_txt=TranslatableString("Select the average number of best tradings you sent each day.",
                                french="Sélectionner le nombre moyen de meilleur échanges réalisés par jour."),
    )


class BestTrading(Trading):
    duration = 4
    traiding_limit = 1
    goods_cost_multiplier = 4
    gold_reward_multiplier = 8
    reward_chest = GoldenChest

    @classmethod
    def daily_income(cls, daily_best_trading_count: float = 0, **kwargs):
        return super().daily_income(daily_trading_count=daily_best_trading_count, **kwargs)

    __display_name = TranslatableString("Best trading", french="Meilleur échange")


# Declare an additional UI parameter for the lottery gains
selected_heroes_param = UIParameter(
    'selected_heroes',
    hero_pair_combinaisons,
    display_range=["{}-{}".format(h1.name[:-4], h2.name[:-4]) for h1, h2 in hero_pair_combinaisons],
    display_txt=TranslatableString("Lottery heroes", french="Héros sélectionnés"),
    help_txt=TranslatableString("Select the pair of heroes selected for your lottery.",
                                french="Sélectionner les deux héros choisis pour la lotterie.")
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
        n = max(0, reset_count_same_day - vip.traiding_quota_free_reset - 1)
        return cls.cumulative_reset_costs[n]

    __display_name = TranslatableString("Trading quota resets", french="Renouvellement du quota d'échange")


class Lottery(Gain):
    """Gain for the three daily free lottery runs, see economy.converters.converters.Lottery for run reward details"""

    @classmethod
    def iteration_income(cls, **kwargs) -> ResourcePacket:
        """Not used"""
        raise NotImplemented()

    @classmethod
    def daily_income(cls, **kwargs) -> ResourcePacket:
        return ResourcePacket(R.LotteryTicket(3))

    __display_name = TranslatableString("Lottery", french="Lotterie")


def update_buidlding_level_param(building_difference_with_hq, hq_lvl):
    return (
        [None] + list(range(1, hq_lvl - building_difference_with_hq + 1)),
        ["Auto (Max)".format()] + ["{} {}".format(lvl, "(HQ {})".format(lvl + building_difference_with_hq)
                                                       if building_difference_with_hq else "")
         for lvl in range(1, hq_lvl - building_difference_with_hq + 1)],
        )


mill_value_range, mill_display_range = update_buidlding_level_param(0, 30)
mill_lvl_param = UIParameter(
    'mill_lvl',
    mill_value_range,
    display_range=mill_display_range,
    default_value=None,
    update_callback=functools.partial(update_buidlding_level_param, 0),
    dependencies=[hq_param],
    display_txt=TranslatableString("Mill", french="Moulin"),
    help_txt=TranslatableString("Select the level of your mill "
                                "\n\n*(AUTO take the maximum level available with your current HQ level)*.",
                                french="Sélectionner le niveau de votre moulin."
                                       "\n\n*(AUTO choisi le niveau maximum disponnible selon votre niveau de QG)*"),
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

    __display_name = TranslatableString("Mill", french="Moulin")


station_value_range, station_display_range = update_buidlding_level_param(0, 30)
station_lvl_param = UIParameter(
    'station_lvl',
    station_value_range,
    display_range=station_display_range,
    default_value=None,
    update_callback=functools.partial(update_buidlding_level_param, 0),
    dependencies=[hq_param],
    display_txt=TranslatableString("Transport station", french="Station de transport"),
    help_txt=TranslatableString(
        "Select the level of your trading station "
        "\n\n*(AUTO take the maximum level available with your current HQ level)*.  "
        "\n*(Note: the transport station production assume that it produces 24/24, so that imply not leaving "
        "it more than 8 hours without collecting gold, so in practice you will probably earn less)*",
        french="Sélectionner le niveau de votre station de transport."
               "\n\n*(AUTO choisi le niveau maximum disponnible selon votre niveau de QG)*  "
               "\n*(Note: le simulateur assume que la station de transport tourne 24h/24, ce qui implqiue de ne jamais"
               "la laisser tourner plus de 8 heures sans récupérer l'or. Donc en pratique vous gagnerez probablement moins)*",
        ),
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


    # TODO The income will probably be partially lost if the player don't play during extended period, thus it may
    #   be more precise to ask for it. Like a daily_collect_count, but it can be miss understood by the user, it
    #   would be better to ask its play hours (or various play strategy (once a day, twice a day, sparsly
    #   all the day, etc.) but all this soon become fairly complex while not adding real value... to meditate on...
    @classmethod
    def daily_income(cls, station_lvl: Optional[int] = None, hq_lvl=1, vip: VIP = 1, daily_collect_count: int = None,
                     **kwargs) -> ResourcePacket:
        income = cls.iteration_income(station_lvl=station_lvl, hq_lvl=hq_lvl, vip=vip, **kwargs) * 12
        if daily_collect_count is not None:
            income = min(income, Mill.storage_limits[station_lvl or hq_lvl] * daily_collect_count)
        return income

    __display_name = TranslatableString("Transport station", french="Station de transport")


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

    __display_name = TranslatableString("Daily quests", french="Quêtes du jour")


class FreeDailyOffer(Gain):

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, **kwargs) -> ResourcePacket:
        return ResourcePacket(R.Goods(rank.traiding_base), R.LifePotion(1))

    @classmethod
    def daily_income(cls, rank: Rank = Rank.NONE, **kwargs) -> ResourcePacket:
        return cls.iteration_income(rank=rank, **kwargs)

    __display_name = TranslatableString("Free daily offer", french="Offre du jour gratuite")


defense_lost_param = UIParameter(
    'defense_lost',
    int,
    display_txt=TranslatableString("Defense lost (daily)", french="Défense par jour"),
    help_txt=TranslatableString(
        "Enter the average number of 100% lost convoy (for example two 50% defense count as one).  "
        "\n*Don't care if it's not really precise, it's already a rought approximation as we wanted to keep it simple. It doesn't have much impact on the overall anyway.*"
        "\n\n*(Note: The simulator compute the worst case where you lost your best tradings first, and that you lost 8 trophy per ambush on average.)*",
        french="Entrer le nombre moyen de convoi 100% perdus par jour (par exemple deux convoi a 50% comptent comme un seul).  "
               "\n*Ne vous creusez pas trop la tête si c'est pas super précis, c'est déjà une grosse approximation et "
               "de toute façon ça a rarement un gros impacte sur votre revenu global.*"
               "\n\n*(Note: Le simulateur choisi le pire scénario, où vos plus gros convois sont toujours attaqués en "
               "premier. Et il compte -8 TR en moyenne par défaite.)*",
        ),

    )

ambush_won_param = UIParameter(
    'ambush_won', 
    int,
    display_txt=TranslatableString("Ambush won", "Embuscades réussies"),
    default_value=20,
    help_txt=TranslatableString(
        "Enter the average number of victorious ambushes you do per day (**including fast ambushes**)."
        "\n\n*(Advice: usually after about 20 successful ambushes per day you do not gain gems, "
        "reincarnation medals, legendary soul nor life potion. You only gain extra cargo, trophy and hero xp.)  "
        "\n(Note: assume you do all your ambushes with a hero in your army and won with 3 stars score)*",
        french="Entrer le nombre moyen d'attaque victorieuse faites par jour (**en incluant les embuscades rapides**)."
               "\n\n*(Conseil: en général le quota maximal journalier de gemmes, médailles de réincarnation, âmes "
               "légendaires et flacon de vie est atteint au bout de 20 attaques environ. Après cela vous ne gagner "
               "plus que des marchandises, de l'xp de héros et des trophés)  "
               "\n(Note: Le simulateur choisi qu'il y a toujours un héro dans votre armée, que vous détruisez toujours "
               "100% du convoi adverse et que vous attaques des joueur du même rang que vous aléatoirement "
               "(c.à.d sans uniquement viser les gros convois de 4h par exemple)*",
        ),
    )

fast_ambushes_param = UIParameter(
    'fast_ambushes',
    range(21),
    display_txt=TranslatableString("Fast Ambushes", french="Embuscades rapides"),
    default_value=0,
    update_callback=lambda ambush_won: (
        range(min(21, ambush_won + 1)),
        [str(n) for n in range(min(21, ambush_won + 1))]
    ),
    dependencies=[ambush_won_param],
    help_txt=TranslatableString(
        "Select the average number of fast ambushes you won per day  "
        "\n*(Note: assume you made 3 stars score on all of them)*",
        french="Sélectionner votre nombre moyen d'embuscade rapide journalière.  "
               "\n*(Note: Le simulateur considère que vous détruisez toujours 100% du convoi)*",
        ),
    )

temple_value_range, temple_display_range = update_buidlding_level_param(6, 30)
temple_lvl_param = UIParameter(
    'temple_lvl',
    temple_value_range,
    display_range=temple_display_range,
    default_value=None,
    update_callback=functools.partial(update_buidlding_level_param, 6),
    display_txt=TranslatableString("Hero shrine level", french="Temple de héros"),
    dependencies=[hq_param],
    help_txt=TranslatableString(
        "Select the level of your hero shrine "
        "\n\n*(AUTO take the maximum level available with your current HQ level)*",
        french="Sélectionner le niveau de votre temple de héros."
               "\n\n*(AUTO choisi le niveau maximum disponnible selon votre niveau de QG)*",
        ),
    )

average_trophy_param = UIParameter(
    'average_trophy',
    [5, 10, 15, 20, 25, 30, 35, 40, 45],
    display_txt=TranslatableString("Average trophy", french="Trophés par attaque"),
    default_value=2,
    help_txt=TranslatableString("Select the average trophy you won on ambushes.",
                                french="Sélectionner le nombre moyen de trophés obtenus par embuscade."),
    )


class Ambushes(Gain):
    _ambush_reward = ResourcePacket(
        R.Gem(8),
        R.LifePotion(1/3),
        R.LegendarySoul(1.13),
        R.ReincarnationToken(1.13),
        ResourceQuantity(RaidChest, 3/10),
        )
    """Reward average expectation per attack (doesn't take daily limits into account)"""
    _max_reward_per_day = ResourcePacket(
        R.Gem(160),
        R.LifePotion(5),
        R.LegendarySoul(26),
        R.ReincarnationToken(26),
        ResourceQuantity(RaidChest, 1),
        )
    # TODO add the 25% gold

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, temple_lvl=None, hq_lvl=1, average_trophy=15, fast_ambushe=False, **kwargs) -> ResourcePacket:
        # This fucntion is not realy used in practice. It's simpler to compute everything into daily_income
        temple_lvl = temple_lvl or hq_lvl
        return (
            cls._ambush_reward
            # Assume all ambush are made with a hero in the army
            + buildings.HeroTemple.ambush_xp_incomes[temple_lvl - 1]
            # Assume that on average you fight against enemies of the same rank as you, and attack 10km, 100km, 100km and best exchangez indiferently
            + R.Goods(rank.traiding_base * 2.5) * (0.75 if fast_ambushe else 1)
            + R.Gold(rank.traiding_base * 2.5) * (0.25 if fast_ambushe else 0)
            + R.Trophy(average_trophy)
        )

    @classmethod
    def daily_income(cls, ambush_won: int = None, rank: Rank = Rank.NONE, temple_lvl=None, hq_lvl=1, average_trophy=15,
                     fast_ambushes: int = 0, **kwargs) -> ResourcePacket:
        temple_lvl = temple_lvl or (hq_lvl - 6)
        if ambush_won is None:
            ambush_won = 20
        return ResourcePacket(
            # Loots of resources with daily limits
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
            # Raid chest (once per day, if there is more than 3 attacks per day)
            ResourceQuantity(RaidChest, 1 if ambush_won > 3 else 0),
            # Guaranted loots (assuming you always have hero in your army)
            #   (Assume all ambush are made with a hero in the army)
            buildings.HeroTemple.ambush_xp_incomes[temple_lvl - 1] * ambush_won,
            R.Trophy(average_trophy * ambush_won),
            # Goods and gold
            #   (Assume that on average you fight against enemies of the same rank as you, and attack
            #   10km, 100km, 100km and best trading indifferently
            R.Goods(rank.traiding_base * 2.5 * (ambush_won - (0.25 * fast_ambushes))),
            R.Gold(rank.traiding_base * 2.5 * (0.25 * fast_ambushes)),
            )

    __display_name = TranslatableString("Ambushes", french="Embuscades")


ask_for_donation_param = UIParameter(
    'ask_for_donation',
    bool,
    display_txt=TranslatableString("Donations received", french="Donnations reçues"),
    default_value=False,
    help_txt=TranslatableString("If you ask for donation in your clan each day, tick this",
                                french="Cocher si vous avez demander tous les jours des donnations de clan."),
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

    __display_name = "Donations"


# TODO daily connection reward

