from __future__ import annotations

import functools
from typing import List, Dict, Set

from dataclasses import dataclass

from Options import Toggle, OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


# Option Dataclass
@dataclass
class CNCGeneralsZHArchipelagoOptions:
    cncgeneralszh_min_skirmish_wins: CNCGeneralsZHMinSkirmishWins
    cncgeneralszh_max_skirmish_wins: CNCGeneralsZHMaxSkirmishWins
    cncgeneralszh_ai_difficulty: CNCGeneralsZHDifficulty
    cncgeneralszh_max_skirmish_map_size: CNCGeneralsZHMaxSkirmishMapSize
    cncgeneralszh_allow_custom_maps: CNCGeneralsZHAllowCustomMaps
    cncgeneralszh_include_campaign: CNCGeneralsZHIncludeCampaign
    cncgeneralszh_include_challenge: CNCGeneralsZHIncludeChallenge
    cncgeneralszh_limit_structures: CNCGeneralsZHLimitStructures
    cncgeneralszh_limit_structures_amount: CNCGeneralsZHLimitStructuresAmount
    cncgeneralszh_limit_units: CNCGeneralsZHLimitUnits
    cncgeneralszh_limit_units_amount: CNCGeneralsZHLimitUnitsAmount

# Main Class
class CNCGeneralsZHGame(Game):
    name = "Command and Conquer: Generals Zero Hour"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = CNCGeneralsZHArchipelagoOptions

    # Optional Game Constraints
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        if not self.banned_structures and not self.banned_units:
            return list()
            
        return [
            # Structures
            GameObjectiveTemplate(
                label="Cannot build these Structures: STRUCTURES",
                data={
                    "STRUCTURES": (self.banned_structures, self.num_banned_structures),
                },
            ),
            # Units
            GameObjectiveTemplate(
                label="Cannot produce these types of Units: UNITS",
                data={
                    "UNITS": (self.banned_units, self.num_banned_units),
                },
            ),
        ]

    # Main Objectives

    # Combine Objectives (Campaign and Challenges)
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = list()
        if self.objective_battlememories:
            objectives += self.campaign_objectives()
        if self.objective_gifts:
            objectives += self.challenge_objectives()

        return objectives

    # Skirmish Objectives
    def skirmish_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a match against these DIFFICULTY armies (separately) as GENERAL, on MAP: AI_GENERALS",
                data={
                    "DIFFICULTY": (self.difficulty, 1),
                    "GENERAL": (self.generals, 1),
                    "MAP": (self.maps, 1),
                    "AI_GENERALS": (self.generals, range(self.min_wins, self.max_wins + 1)),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            )
        ]

    # Campaign Objectives
    def campaign_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete the CAMPAIGN, on DIFFICULTY difficulty",
                data={
                    "CAMPAIGN": (self.campaigns, 1),
                    "DIFFICULTY": (self.difficulty, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            )
        ]

    # Challenge Objectives
    def campaign_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete the GENERAL Challenge, on DIFFICULTY difficulty",
                data={
                    "GENERAL": (self.challenges, 1),
                    "DIFFICULTY": (self.difficulty, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            )
        ]

    # Datasets

    # Maps
    @functools.cached_property
    def maps_2(self) -> List[str]:
        return [
            "Alpine Assault (2)",
            "Barren Badlands (2)",
            "Bitter Winter (2)",
            "Bombardment Beach (2)",
            "Desert Fury (2)",
            "Dust Devil (2)",
            "Final Crusade (2)",
            "Flash Fire (2)",
            "Forgotten Forest (2)",
            "Heartland Shield (2)",
            "Killing Fields (2)",
            "Leipzig Lowlands (2)",
            "North America (2)",
            "Sand Serpent (2)",
            "Seaside Mutiny (2)",
            "Silent River (2)",
            "The Frontline (2)",
            "Tournament Desert (2)",
            "Tournament Plains (2)",
            "Wasteland Warlords (2)",
            "Winding River (2)",
            "Winter Wolf (2)",
        ]
    
    @functools.cached_property
    def maps_3(self) -> List[str]:
        return [
            "Cairo Commandos (3)",
            "Flash Effect (3)",
        ]
    
    @functools.cached_property
    def maps_4(self) -> List[str]:
        return [
            "Bear Town Beatdown (4)",
            "Dark Mountain (4)",
            "Dark Night (4)",
            "Dogs of War (4)",
            "Eastern Everglades (4)",
            "El Scorcho (4)",
            "Fallen Empire (4)",
            "Flooded Plains (4)",
            "Golden Oasis (4)",
            "Homeland Alliance (4)",
            "Lights Out (4)",
            "Lone Eagle (4)",
            "Manic Aggression (4)",
            "Mountain Fox (4)",
            "Overland Offensive (4)",
            "Rocky Rampage (4)",
            "Rogue Agent (4)",
            "Tournament A (4)",
            "Tournament B (4)",
            "Tournament Continent (4)",
            "Tournament Island (4)",
            "Tournament Lake (4)",
            "Tournament Tundra (4)",
            "Tournament Urban (4)",
            "Victory Valley (4)",
        ]

    @functools.cached_property
    def maps_5(self) -> List[str]:
        return [
            "Mountain Guns (5)",
        ]

    @functools.cached_property
    def maps_6(self) -> List[str]:
        return [
            "Defcon 6 (6)",
            "Free Fire Zone (6)",
            "Green Pastures (6)",
            "Hostile Dawn (6)",
            "Red Rock (6)",
            "Tournament City (6)",
        ]

    @functools.cached_property
    def maps_7(self) -> List[str]:
        return []

    @functools.cached_property
    def maps_8(self) -> List[str]:
        return [
            "Death Valley (8)",
            "Destruction Station (8)",
            "Fortress Avalanche (8)",
            "Iron Dragon (8)",
            "Twilight Flame (8)",
            "Whiteout (8)",
        ]
    
    def maps(self) -> List[str]:
        maps: List[str] = self.maps_2[:]

        # Iteratively add maps based on max_map_size, starting from 3
        for size in range(3, self.max_map_size + 1):
            map_list = getattr(self, f'maps_{size}')
            maps.extend(map_list[:])

        return sorted(maps)

    # Generals
    @staticmethod
    def generals() -> List[str]:
        return [
            "Any General"
            "Random General"
            "USA (No General)",
            "USA Super Weapon General",
            "USA Laser General",
            "USA Air Force General",
            "China (No General)",
            "China Tank General",
            "China Infantry General",
            "China Nuke General",
            "GLA (No General)",
            "GLA Toxin General",
            "GLA Demolition General",
            "GLA Stealth General",
        ]

    # Campaigns
    @staticmethod
    def campaigns() -> List[str]:
        return [
            "USA Campaign",
            "China Campaign",
            "GLA Campaign",
        ]

    # Challenges
    @staticmethod
    def challenges() -> List[str]:
        return [
            "USA Super Weapon General's",
            "USA Laser General's",
            "USA Air Force General's",
            "China Tank General's",
            "China Infantry General's",
            "China Nuke General's",
            "GLA Toxin General's",
            "GLA Demolition General's",
            "GLA Stealth General's",
        ]

    # Min Skirmish Wins
    @property
    def min_wins(self) -> int:
        return int(self.archipelago_options.cncgeneralszh_min_skirmish_wins.value)

    # Max Skirmish Wins
    @property
    def max_wins(self) -> int:
        return int(self.archipelago_options.cncgeneralszh_max_skirmish_wins.value)

    # AI Difficulty
    @property
    def difficulty(self) -> str:
        return str(self.archipelago_options.cncgeneralszh_ai_difficulty.value)

    # Max Skirmish Map Size
    @property
    def max_map_size(self) -> int:
        return int(self.archipelago_options.CNCGeneralsZHMaxSkirmishMapSize.value)

    # Allow Custom Maps
    @property
    def include_custom(self) -> bool:
        return bool(self.archipelago_options.CNCGeneralsZHMaxSkirmishMapSize.value)

    # Include Campaign
    @property
    def include_campaign(self) -> bool:
        return bool(self.archipelago_options.CNCGeneralsZHIncludeCampaign.value)

    # Include Challenge
    @property
    def include_challenge(self) -> bool:
        return bool(self.archipelago_options.CNCGeneralsZHIncludeChallenge.value)

    # Banned Structures/Buildings
    @property
    def banned_structures(self) -> Set[str]:
        return self.archipelago_options.CNCGeneralsZHLimitStructures.value

    # Banned Units
    @property
    def banned_units(self) -> Set[str]:
        return self.archipelago_options.CNCGeneralsZHLimitUnits.value

    # Banned Structure/Building Amount
    @property
    def num_banned_structures(self) -> int:
        return int(self.archipelago_options.CNCGeneralsZHLimitStructuresAmount.value)

    # Banned Unit Amount
    @property
    def num_banned_units(self) -> int:
        return int(self.archipelago_options.CNCGeneralsZHLimitUnitsAmount.value)

# Archipelago Options
class CNCGeneralsZHMinSkirmishWins(NamedRange):
    """
    Specifies the minimum number of wins needed for Skirmish matches when generating objectives.
    Specify a number from 1-5 or pick from the named options below.
    - normal: 1 win
    - extreme: 3 wins
    - extreme: 5 wins
    - random: Randomized minimum from 1 to 5 wins
    **DOES NOT CHECK IF MIN IS GREATER THAN MAX!**
    """

    rich_text_doc = True
    range_start = 1
    range_end = 5
    special_range_names = {
        "normal": 1,
        "long": 3,
        "extreme": 5,
        "random": random,
    }

    default = 1

    display_name = "Command and Conquer: Generals Zero Hour Min Skirmish Wins"

class CNCGeneralsZHMaxSkirmishWins(NamedRange):
    """
    Specifies the maximum number of wins needed for Skirmish matches when generating objectives.
    Specify a number from 1-5 or pick from the named options below.
    - normal: 1 win
    - extreme: 3 wins
    - extreme: 5 wins
    - random: Randomized maximum from 1 to 5 wins
    **DOES NOT CHECK IF MAX IS LESS THAN MIN!**
    """

    rich_text_doc = True
    range_start = 1
    range_end = 5
    special_range_names = {
        "normal": 1,
        "long": 3,
        "extreme": 5,
        "random": random,
    }

    default = 2

    display_name = "Command and Conquer: Generals Zero Hour Max Skirmish Wins"

class CNCGeneralsZHDifficulty(Choice):
    """Sets difficulty of Enemy AI armies in ALL gamemodes. Defaults to Normal.

    - **Easy:**
    - **Normal:**
    - **Hard:**"""
    display_name = "Difficulty"
    rich_text_doc = True
    option_easy = 0
    option_normal = 1
    option_hard = 2
    default = 1

    display_name = "Command and Conquer: Generals Zero Hour AI Difficulty"

class CNCGeneralsZHMaxSkirmishMapSize(Range):
    """
    Indicates the max map size for Skirmish matches when generating objectives.
    Range is from 2 to 8. 
    Assumes that each slot is filled with an AI army on Team None (or for multiplayer, equal sized teams as human players).
    You can choose if the AI armies are all the same as the one specified in the objective or just one of them are the specified AI general.
    """

    display_name = "Command and Conquer: Generals Zero Hour Max Skirmish Map Size"

class CNCGeneralsZHAllowCustomMaps(Toggle):
    """
    Indicates whether to allow custom maps for Skirmish matches when generating objectives.
    Custom Maps will have 50% weight for any Skirmish objectives.
    """

    display_name = "Command and Conquer: Generals Zero Hour Allow Custom Maps"
    
class CNCGeneralsZHIncludeCampaign(Toggle):
    """
    Indicates whether to include Challenge Missions (Missions 1-5, start to finish) when generating objectives.
    """

    display_name = "Command and Conquer: Generals Zero Hour Include Campaign Levels"

class CNCGeneralsZHIncludeChallenge(Toggle):
    """
    Indicates whether to include Challenge Missions (Missions 1-7, start to finish) when generating objectives.
    """

    display_name = "Command and Conquer: Generals Zero Hour Include Challenge Missions"

class CNCGeneralsZHLimitStructures(OptionSet):
    """
    Bans the use of a randomized building/structure when generating objectives.
    Provide a List of strings for each building/structure you'd like to include as a potential ban.
    **DOES NOT CHECK FOR LOGICAL COMPLETION!**

    Valid Buildings/Structures:
    - Barracks
    - War Factory
    - Base Defenses
    - Air Field
    - Strategy Buildings
    - Alt. Money Buildings
    - Superweapons
    """

    rich_text_doc = True
    valid_keys_casefold = True
    valid_keys = [
        "Barracks",
        "War Factory",
        "Base Defenses",
        "Air Field",
        "Strategy Buildings",
        "Alt. Money Buildings",
        "Superweapons"
    ]

    default = []

    display_name = "Command and Conquer: Generals Zero Hour Limit Structures"

class CNCGeneralsZHLimitStructuresAmount(NamedRange):
    """
    Specifies the number of randomized building/structure bans when generating objectives.
    Specify a number from 1-5, pick from the named options below, or **leave blank for no bans**.
    - normal: 1 ban
    - extreme: 3 bans
    - random: Randomized from 1 to 5 bans
    Limited to up to 5 for some possibility of completion.
    **DOES NOT CHECK FOR LOGICAL COMPLETION!**
    **DOES NOT CHECK IF PROVIDED NUMBER EXCEEDS PROVIDED LIST SIZE!**
    """

    rich_text_doc = True
    range_start = 1
    range_end = 5
    special_range_names = {
        "normal": 1,
        "extreme": 3,
        "random": random,
    }

    default = 0

    display_name = "Command and Conquer: Generals Zero Hour Limit Structures Amount"

class CNCGeneralsZHLimitUnits(OptionSet):
    """
    Bans the use of a randomized type of unit when generating objectives.
    Provide a List of strings for each type of unit you'd like to include as a potential ban.
    **DOES NOT CHECK FOR LOGICAL COMPLETION!**

    Valid Units:
    - Rifle Infantry
    - Rocket Infantry
    - Standard Tanks
    - Artillery + Avengers
    - Plane-Type Aircraft
    - Comanches/Helixes
    - Infantry Vehicles
    - Machine Gun Vehicles
    """

    rich_text_doc = True
    valid_keys_casefold = True
    valid_keys = [
        "Rifle Infantry",
        "Rocket Infantry",
        "Standard Tanks",
        "Artillery + Avengers",
        "Plane-Type Aircraft",
        "Comanches/Helixes",
        "Infantry Vehicles",
        "Machine Gun Vehicles"
    ]

    default = []

    display_name = "Command and Conquer: Generals Zero Hour Limit Units"

class CNCGeneralsZHLimitUnitsAmount(NamedRange):
    """
    Specifies the number of randomized unit bans when generating objectives.
    Specify a number from 1-5, pick from the named options below, or **leave blank for no bans**.
    - normal: 1 ban
    - extreme: 3 bans
    - random: Randomized from 1 to 5 bans
    Limited to up to 5 for some possibility of completion.
    **DOES NOT CHECK FOR LOGICAL COMPLETION!**
    **DOES NOT CHECK IF PROVIDED NUMBER EXCEEDS PROVIDED LIST SIZE!**
    """

    rich_text_doc = True
    range_start = 1
    range_end = 5
    special_range_names = {
        "normal": 1,
        "extreme": 3,
        "random": random,
    }

    default = 0

    display_name = "Command and Conquer: Generals Zero Hour Limit Units Amount"