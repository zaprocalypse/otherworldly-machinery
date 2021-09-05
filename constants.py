from PIL import ImageFont
STAT_LOOKUP_TABLE = {
    'CriticalHitDamagePercent': 'CD%:',
    'CriticalHitChancePercent': 'CC%:',
    'Speed': 'Speed:',
    'EffectivenessPercent': 'Eff:',
    'EffectResistancePercent': 'Res:',
    'Health': 'Health:',
    'HealthPercent': 'Health%:',
    'DefensePercent': 'Def%:',
    'Defense': 'Def:',
    'Attack': 'Attack:',
    'AttackPercent': 'Attack%:'
}

IMPRINT_LOOKUP = {
    'att_rate':'% Atk',
    'att':' Atk',
    'def_rate':'% Def',
    'def':' Def',
    'cri':' % CC',
    'speed':' speed',
    'max_hp_rate':'% HP',
    'max_hp':' HP',
    'acc':'% Eff',
    'res':'% Res',
    'coop':'% Dual'
}

NEW_SET_LOOKUP_TABLE = {
    'SpeedSet':4,
    'HitSet':2,
    'CriticalSet':2,
    'AttackSet':4,
    'ImmunitySet':2,
    'DefenseSet':2,
    'HealthSet':2,
    'DestructionSet':4,
    'ResistSet':2,
    'RageSet':4,
    'LifestealSet':4,
    'UnitySet':2,
    'InjurySet':4,
    'RevengeSet':4,
    'PenetrationSet':2,
    'CounterSet':4
}



SET_LOOKUP_TABLE = {
    0: {'set': 'health', 'size': 2},
    1: {'set': 'defense', 'size': 2},
    2: {'set': 'attack', 'size': 4},
    3: {'set': 'speed', 'size': 4},
    4: {'set': 'critical', 'size': 2},
    5: {'set': 'hit', 'size': 2},
    6: {'set': 'destruction', 'size': 4},
    7: {'set': 'lifesteal', 'size': 4},
    8: {'set': 'counter', 'size': 4},
    9: {'set': 'resistance', 'size': 2},
    10: {'set': 'unity', 'size': 2},
    11: {'set': 'rage', 'size': 4},
    12: {'set': 'immunity', 'size': 2},
    13: {'set': 'penetration', 'size': 2},
    14: {'set': 'revenge', 'size': 4},
    15: {'set': 'injury', 'size': 4},
}

RARITY_COLOUR_LOOKUP_TABLE = {
    'Epic': (255, 0, 0),
    'Heroic': (106, 13, 173),
    'Rare': (0, 0, 255),
    'Good': (144, 238, 144),
    'Normal': (128, 128, 128)
}

ELEMENT_COLOUR_LOOKUP_TABLE = {
    'dark': (183, 71, 185),
    'earth': (141, 208, 44),
    'ice': (48, 198, 255),
    'fire': (230, 67, 50),
    'light': (255, 202, 53)
}

# Set of image used to represent list
SET_IMAGE_SIZE = (20, 20)

# Or that equipment should be displayed in
EQUIP_LIST_ORDER = ['Weapon', 'Helmet', 'Armor', 'Necklace', 'Ring', 'Boots']

# Text colour filled as white
FILL_WHITE = (255, 255, 255)

font_file = 'assets\\Fira_Sans_Condensed\\FiraSansCondensed-Regular.ttf'
FNT = ImageFont.truetype(font_file, 12)
FNT2 = ImageFont.truetype(font_file, 28)
FN2SMALL = ImageFont.truetype(font_file, 18)
FN2VSMALL = ImageFont.truetype(font_file, 14)
FNT3 = ImageFont.truetype(font_file, 16)
FNT4 = ImageFont.truetype(font_file, 12)
FNT5 = ImageFont.truetype(font_file, 8)
ARTIFACT_FNT = ImageFont.truetype(font_file, 10)
FNT6 = ImageFont.truetype(font_file, 22)
FNT7 = ImageFont.truetype(font_file, 10)
