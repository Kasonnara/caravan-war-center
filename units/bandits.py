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
from buildings.buildings import Camp
from common.card_categories import BANDITS
from common.rarity import Rarity
from common.resources import resourcepackets_gold
from units.base_units import MovableUnit, AOE, reincarnation
from common.target_types import TargetType
from units.vehicles import Vehicle


class Bandit(MovableUnit):
    base_building = Camp


class Maraudeur(Bandit):
    hp_base = 451
    attack_base = 120
    hit_frequency = 0.4
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 2
    armor_piercing = 0
    cost = 3
    move_speed = 1.7
    rarity = Rarity.Common
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        -56000,
        )


class Archer(Bandit):
    hp_base = 300
    attack_base = 71
    hit_frequency = 1
    range = 8
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 3
    move_speed = 1.7
    rarity = Rarity.Common
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        -68000,
        )


class Drone(Bandit):
    hp_base = 500
    attack_base = 95
    hit_frequency = 0.75
    range = 3
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 0
    armor_piercing = 0
    cost = 3
    move_speed = 2
    rarity = Rarity.Common
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, -32000,  # 1 -> 6
        )


class Brute(Bandit):
    hp_base = 1125
    attack_base = 130
    hit_frequency = 0.5
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 4
    move_speed = 1.6
    rarity = Rarity.Rare
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,       # 1 -> 6
        None, None, None, None, None,       # 6 -> 11
        None, None, None, None, -10240000,  # 11 -> 16
        )


class Lutin(Bandit):
    hp_base = 650
    attack_base = 110
    hit_frequency = 0.8
    range = 4
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 0
    armor_piercing = 0
    cost = 6
    move_speed = 1.9
    rarity = Rarity.Rare
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,       # 1 -> 6
        None, None, None, None, None,       # 6 -> 11
        None, None, -3840000, -6590000, -11440000,
        )


class Berserk(Bandit):
    hp_base = 960
    attack_base = 150
    hit_frequency = 0.6
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 4
    armor_piercing = 0
    cost = 4
    move_speed = 1.8
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        None, None, None, None, None,  # 6 -> 11
        -1180000, -2060000, -3640000, -6240000
        )


class Hunter(Bandit):
    hp_base = 500
    attack_base = 122
    hit_frequency = 0.6
    range = 9
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 3
    cost = 4
    move_speed = 1.5
    rarity = Rarity.Rare
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        None, None, None, None, None,  # 6 -> 11
        None, None, None, -6930000, -12040000,
        )


class Spider(AOE, Bandit):
    hp_base = 1140
    attack_base = 110
    hit_frequency = 0.35
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 4
    move_speed = 1.4
    rarity = Rarity.Rare
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,      # 1 -> 6
        None, None, None, None, None,      # 6 -> 11
        None, None, None, None, -11440000  # 11 -> 16
        )


class Alchimist(AOE, Bandit):
    hp_base = 482
    attack_base = 140
    hit_frequency = 0.4
    range = 4
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 5
    move_speed = 1.6
    rarity = Rarity.Rare
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,       # 1 -> 6
        None, None, None, None, None,       # 6 -> 11
        None, None, None, None, -12040000,  # 11 -> 16
        )


class Viking(Bandit):
    hp_base = 1900
    attack_base = 200
    hit_frequency = 1
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 6
    armor_piercing = 2
    cost = 8
    move_speed = 1.9
    consecutive_hit_attack_boost = 0.4
    max_consecutive_boost = 3.
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,
        None, None, None, None, None,  # 6 -> 11
        None, None, -5670000, -9710000, -16860000,
        )


@reincarnation
class VikingLeg(Viking):
    hit_frequency = 1.25
    # FIXME: viking combo doesn't behave like other combo


class Momie(Bandit):
    hp_base = 1400
    attack_base = 240
    hit_frequency = 0.6
    range = 7
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 7
    move_speed = 1.4
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        None, None, None, None, -950000,  # 6 -> 11
        -1770000, -3100000, -5460000, -9360000, -16260000,
        )


@reincarnation
class MomieLeg(Momie):
    pass


class DarkKnight(Bandit):
    hp_base = 1677
    attack_base = 394
    hit_frequency = 0.8
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 6
    armor_piercing = 0
    cost = 8
    move_speed = 1.9
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,        # 1 -> 6
        None, None, None, None, -1020000,    # 6 -> 11
        -1900000, -3330000, -5870000, -10050000, -17460000,
        )


@reincarnation
class DarkKnightLeg(DarkKnight):
    stun_duration = 2.5


class Condor(Bandit):
    hp_base = 1469
    attack_base = 260
    hit_frequency = 0.7
    range = 8
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.AIR
    armor = 0
    armor_piercing = 0
    cost = 8
    move_speed = 1.7
    armor_reduction = 5
    spell_duration = 60
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0, # 0 -> 1
        None, None, None, None, None,        # 1 -> 6
        None, None, None, None, -1050000,    # 6 -> 11
        -1970000, -3440000, -6070000,
        )


@reincarnation
class CondorLeg(Condor):
    armor_reduction = 100


class Stealer(Bandit):
    hp_base = 1430
    attack_base = 328
    hit_frequency = 0.9
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 3
    armor_piercing = 2
    cost = 7
    move_speed = 2
    vehicule_damage_factor = 2  # Fixme: check if it's "200% damages" or "200% additional damages"
    rarity = Rarity.Epic

    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,           # 1 -> 6
        None, None, None, None, None,           # 6 -> 11
        None, None, -6070000, -10400000, -18070000,  # 11 -> 16
        )

    # TODO: invisibility effect

    def damage_formule(self, target: MovableUnit, target_index=0, hit_combo=0):
        dmg = super().damage_formule(target, target_index, hit_combo)
        if dmg is None:
            return None
        if isinstance(target, Vehicle):
            return dmg * self.vehicule_damage_factor
        else:
            return dmg


@reincarnation
class StealerLeg(Stealer):
    hit_frequency = 1.2
    shoot_to = TargetType.AIR_GROUND
    vehicule_damage_factor = 2.5


class Lich(Bandit):
    hp_base = 1072
    attack_base = 390
    hit_frequency = 0.4
    range = 5
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 6
    cost = 8
    move_speed = 1
    summon_number = 3
    summon_hp_base = 455
    summon_attack_base = 38
    summon_atk_speed = 1 / 10
    rarity = Rarity.Epic
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        None, None, None, None, -980000,  # 6 -> 11
        None, -3210000,
        )


@reincarnation
class LichLeg(Lich):
    summon_number = 5
    summon_atk_speed = 1 / 7


class Inferno(Bandit):
    hp_base = 4407
    attack_base = 630
    hit_frequency = 0.7
    range = 1
    shoot_to = TargetType.GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 12
    move_speed = 1.7
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        None, None, None, None, None,  # 6 -> 11
        None, -5160000,
        )


class Demon(Bandit):
    hp_base = 3900
    attack_base = 500
    hit_frequency = 1
    range = 2
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 8
    armor_piercing = 4
    cost = 10
    move_speed = 1.9
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,            # 1 -> 6
        None, None, None, None, None,            # 6 -> 11
        None, None, -8500000, -14560000, -25290000,  # 11 -> 16
        )


class Chaman(Bandit):
    hp_base = 1605
    attack_base = 504
    hit_frequency = 0.5
    range = 8
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 3
    cost = 12
    move_speed = 1.4
    rarity = Rarity.Legendary
    # TODO heal effect
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        None, None, None, None, None,  # 6 -> 11
        None, -4590000, -8090000, -13860000, -24090000,
        )


class Djin(Bandit, AOE):
    hp_base = 1456
    attack_base = 370
    hit_frequency = 0.5
    range = 6
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 0
    armor_piercing = 0
    cost = 11
    move_speed = 1.3
    summon_number = 1
    summon_hp = {8: 2627}
    summon_atk = {8: 450}
    summon_atk_speed = 1 / 10
    # TODO Slow down effect
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        None, None, None, None, None,  # 6 -> 11
        None, None, -8300000, -14210000, -24690000,
        )


class Mecha(Bandit):
    hp_base = 1885
    attack_base = 331
    hit_frequency = 0.6
    range = 7
    shoot_to = TargetType.AIR_GROUND
    shooted_as = TargetType.GROUND
    armor = 6
    armor_piercing = 0
    cost = 11
    move_speed = 1.5
    multiple_target_limit = 3
    missil_attack_base = 374
    missile_atk_speed = 0.5
    # TODO missile
    rarity = Rarity.Legendary
    upgrade_costs = resourcepackets_gold(
        0,  # 0 -> 1
        None, None, None, None, None,  # 1 -> 6
        None, None, None, None, None,  # 6 -> 11
        None, None, None, -14900000, -25890000
        )


# Register all defined cards
BANDITS.register_cards_in_module(Bandit, __name__)
