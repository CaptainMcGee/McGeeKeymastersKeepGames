from __future__ import annotations

import functools
from typing import List, Dict, Set

from dataclasses import dataclass

from Options import Toggle, OptionSet, NamedRange, TextChoice, Range

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


# Option Dataclass
@dataclass
class CNCGeneralsZHArchipelagoOptions:
    generals_zh_ai_difficulty: CNCGeneralsZHDifficulty
    generals_zh_max_skirmish_map_size: CNCGeneralsZHMaxSkirmishMapSize
    generals_zh_include_campaign: CNCGeneralsZHIncludeCampaign
    generals_zh_include_challenge: CNCGeneralsZHIncludeChallenge
    generals_zh_limit_structures: CNCGeneralsZHLimitStructures
    generals_zh_limit_structures_amount: CNCGeneralsZHLimitStructuresAmount
    generals_zh_limit_units: CNCGeneralsZHLimitUnits
    generals_zh_limit_units_amount: CNCGeneralsZHLimitUnitsAmount

# Main Class
class CNCGeneralsZHGame(Game):
    name = "Command and Conquer: Generals Zero Hour"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = CNCGeneralsZHArchipelagoOptions

    # Optional Game Constraints
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        constraints: List[GameObjectiveTemplate] = list()
        if self.banned_structures and (self.archipelago_options.generals_zh_limit_structures_amount.value > 0):
            constraints += self.structure_constraints()
        if self.banned_units and (self.archipelago_options.generals_zh_limit_structures_amount.value > 0):
            constraints += self.unit_constraints()

        return constraints
    
    def structure_constraints(self) -> List[GameObjectiveTemplate]:
        # temp = self.num_banned_structures
        return [
            # Structures
            GameObjectiveTemplate(
                label="Cannot build these Structures: STRUCTURES",
                data={
                    "STRUCTURES": (self.structures, self.archipelago_options.generals_zh_limit_structures_amount.value),
                },
            ),
        ]
    
    def unit_constraints(self) -> List[GameObjectiveTemplate]:
        return [
            # Units
            GameObjectiveTemplate(
                label="Cannot produce these types of Units: UNITS",
                data={
                    "UNITS": (self.units, self.archipelago_options.generals_zh_limit_units_amount.value),
                },
            ),
        ]

    # Main Objectives

    # Combine Objectives (Campaign and Challenges)
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = list()
        objectives += self.skirmish_objectives()
        if self.include_campaign:
            objectives += self.campaign_objectives()
        if self.include_challenge:
            objectives += self.challenge_objectives()

        return objectives

    # Skirmish Objectives
    def skirmish_objectives(self) -> List[GameObjectiveTemplate]:
        # num_matches = 
        return [
            GameObjectiveTemplate(
                label="Win MATCHES matches against a DIFFICULTY AI army, as GENERAL, on MAP",
                data={
                    "MATCHES": (self.matches, 1),
                    "DIFFICULTY": (self.difficulty, 1),
                    "GENERAL": (self.generals, 1),
                    "MAP": (self.maps, 1),
                    "AI": (self.generals, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
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
    def challenge_objectives(self) -> List[GameObjectiveTemplate]:
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
        if self.archipelago_options.generals_zh_max_skirmish_map_size.value >= 3:
        #   maps.extend(self.maps_8) 
            for size in range(3, self.archipelago_options.generals_zh_max_skirmish_map_size.value + 1):
                map_list = getattr(self, f'maps_{size}')
                maps.extend(map_list[:])

        return sorted(maps)

    # Generals
    @staticmethod
    def generals() -> List[str]:
        return [
            "**YOU PICK**",
            "Random General",
            "USA",
            "USA Super Weapon General",
            "USA Laser General",
            "USA Air Force General",
            "China",
            "China Tank General",
            "China Infantry General",
            "China Nuke General",
            "GLA",
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

    # Number of Matches
    # @staticmethod
    
    # def num_matches() -> range:
    #    return range(1, 4)

    @staticmethod
    def matches() -> range:
        return range(1,4)
    
    # AI Difficulty
    @property
    def ai_difficulty(self) -> Set[str]:
        return self.archipelago_options.generals_zh_ai_difficulty.value
    
    def difficulty(self) -> List[str]:
        return sorted(self.ai_difficulty)

    # Include Campaign
    @property
    def include_campaign(self) -> bool:
        return self.archipelago_options.generals_zh_include_campaign

    # Include Challenge
    @property
    def include_challenge(self) -> bool:
        return self.archipelago_options.generals_zh_include_challenge

    # Banned Structures/Buildings
    @property
    def banned_structures(self) -> Set[str]:
        return self.archipelago_options.generals_zh_limit_structures.value
    
    def structures(self) -> List[str]:
        return sorted(self.banned_structures)

    # Banned Units
    @property
    def banned_units(self) -> Set[str]:
        return self.archipelago_options.generals_zh_limit_units.value
    
    def units(self) -> List[str]:
        return sorted(self.banned_units)



# Archipelago Options

class CNCGeneralsZHDifficulty(OptionSet):
    """Indicates the range of difficulties of Enemy AI armies in ALL gamemodes. Accepts multiple difficulty options. Defaults to just Normal.

    Valid Difficulties:
    - Easy
    - Normal
    - Hard

    Example Input: ['Easy','Normal','Hard']
    """

    valid_keys = [
        "Easy",
        "Normal",
        "Hard",
    ]

    default = ["Normal"]

    display_name = "Command and Conquer: Generals Zero Hour AI Difficulty"

class CNCGeneralsZHMaxSkirmishMapSize(NamedRange):
    """
    Indicates the max map size for Skirmish matches when generating objectives.
    Range is from 2 to 8. Defaults to 2.
    Assumes that each slot is filled with an AI army on Team None (or for multiplayer, equally sized teams as human players).
    You can choose if the AI armies are all the same general as the one specified in the objective or just one of them are the specified AI general.
    """

    rich_text_doc = True
    range_start = 2
    range_end = 8
    special_range_names = {
        "duel": 2,
        "smallteams": 4,
        "largeteams": 8,
    }

    default = 2

    display_name = "Command and Conquer: Generals Zero Hour Max Skirmish Map Size"
    
class CNCGeneralsZHIncludeCampaign(Toggle):
    """
    Indicates whether to include Challenge Missions (Missions 1-5, start to finish) when generating objectives. Defaults to False.
    """

    display_name = "Command and Conquer: Generals Zero Hour Include Campaign Levels"

class CNCGeneralsZHIncludeChallenge(Toggle):
    """
    Indicates whether to include Challenge Missions (Missions 1-7, start to finish) when generating objectives. Defaults to False.
    """

    display_name = "Command and Conquer: Generals Zero Hour Include Challenge Missions"

class CNCGeneralsZHLimitStructures(OptionSet):
    """
    POTENTIALLY bans the use of a randomized building/structure when generating objectives.
    Provide a List of strings for each building/structure you'd like to include as a potential ban.
    **DOES NOT CHECK FOR LOGICAL COMPLETION!**

    Valid Buildings/Structures:
    - Base Defenses
    - Air Field
    - Strategy Buildings (Strategy Center, Propaganda Tower, Palace)
    - Alt. Money Buildings (Supply Drop Zone, Internet Center, Black Market)
    - Superweapons

    Example Input: ['Strategy Buildings','Alt. Money Buildings','Superweapons']
    """

    valid_keys = [
        "Base Defenses",
        "Air Field",
        "Strategy Buildings",
        "Alt. Money Buildings",
        "Superweapons",
    ]

    default = valid_keys

    display_name = "Command and Conquer: Generals Zero Hour Limit Structures"

class CNCGeneralsZHLimitStructuresAmount(NamedRange):
    """
    Specifies the number of randomized building/structure bans when generating objectives.
    Specify a number from 1-5, pick from the named options below, or **leave as is for no bans**.
    - none: no bans
    - normal: 1 ban
    - extreme: 3 bans
    - impossible: 5 bans
    **DOES NOT CHECK FOR LOGICAL COMPLETION!**
    **DOES NOT CHECK IF PROVIDED NUMBER EXCEEDS PROVIDED LIST SIZE!**
    """

    rich_text_doc = True
    range_start = 1
    range_end = 5
    special_range_names = {
        "none": 0,
        "normal": 1,
        "extreme": 3,
        "impossible": 5,
    }

    default = 0

    display_name = "Command and Conquer: Generals Zero Hour Limit Structures Amount"

class CNCGeneralsZHLimitUnits(OptionSet):
    """
    POTENTIALLY bans the use of a randomized type of unit when generating objectives.
    Provide a List of strings for each type of unit you'd like to include as a potential ban.
    **DOES NOT CHECK FOR LOGICAL COMPLETION!**

    Valid Units (Detailed Descriptions within parentheses, don't put these in input)
    - Rifle Infantry (Ranger, Red Guard, Mini-Gunner, Rebel)
    - Rocket Infantry (Missile Defender, Tank Hunter, RPG Trooper)
    - Infantry Vehicles (Humvee, Troop Crawler, Assault/Listening Outpost, Technical, Combat Cycle, Battle Bus)
    - Tanks (Crusader, Laser Tank, Paladin, Battlemaster, Dragon Tank, Overlord, Scorpion, Marauder)
    - Machine Gun Vehicles (Gatling Cannon, Quad Cannon)
    - Artillery + Avengers (Tomahawk, Inferno Cannon, Nuke Cannon, SCUD Launcher, Avengers)
    - Plane-Type Aircraft (Raptor, Stealth Figther, Aurora, MiG Fighter)
    - Comanches/Helixes

    Example Input: ['Tanks','Artillery + Avengers','Plane-Type Aircraft','Infantry Vehicles']
    """

    valid_keys = [
        "Rifle Infantry",
        "Rocket Infantry",
        "Infantry Vehicles",
        "Tanks",
        "Machine Gun Vehicles",
        "Artillery + Avengers",
        "Plane-Type Aircraft",
        "Comanches/Helixes",
    ]

    default = valid_keys

    display_name = "Command and Conquer: Generals Zero Hour Limit Units"

class CNCGeneralsZHLimitUnitsAmount(NamedRange):
    """
    Specifies the number of randomized unit bans when generating objectives.
    Specify a number from 1-5, pick from the named options below, or **leave as is for no bans**.
    - none: no bans
    - normal: 1 ban
    - extreme: 3 bans
    - impossible: 5 bans
    Limited to up to 5.
    **DOES NOT CHECK FOR LOGICAL COMPLETION!**
    **DOES NOT CHECK IF PROVIDED NUMBER EXCEEDS PROVIDED LIST SIZE!**
    """

    rich_text_doc = True
    range_start = 1
    range_end = 5
    special_range_names = {
        "none": 0,
        "normal": 1,
        "extreme": 3,
        "impossible": 5,
    }

    default = 0

    display_name = "Command and Conquer: Generals Zero Hour Limit Units Amount"