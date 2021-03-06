# 无弹药数的武器分组
SLOT_NO_AMMO = [0, 1]

WEAPON_NONE = ( 0, 0, "无" )

WEAPON_LIST = [
    [
        # (id, model, name)
        WEAPON_NONE,
    ],
    [
        # MELEE = 1
        WEAPON_NONE,
        (1, 0, "棒球棍"),
        (2, 0, "桌球杆"),
        (3, 0, "小刀"),
    ],
    [
        # HANDGUN = 2
        WEAPON_NONE,
        (7, 0, "手枪"),
        (9, 0, "沙漠之鹰"),
    ],
    [
        # SHOTGUN = 3
        WEAPON_NONE,
        (10, 0, "短管猎枪"),
        (11, 0, "贝雷塔猎枪"),
    ],
    [
        # SMG = 4
        WEAPON_NONE,
        (12, 0, "乌兹微冲"),
        (13, 0, "MP5"),
    ],
    [
        # RIFLE = 5
        WEAPON_NONE,
        (14, 0, "AK47"),
        (15, 0, "M4"),
    ],
    [
        # SNIPER = 6
        WEAPON_NONE,
        (16, 0, "狙击步枪"),
        (17, 0, "M40A1"),
    ],
    [
        # HEAVY = 7
        WEAPON_NONE,
        (18, 0, "火箭发射器"),
        (20, 0, "机枪"),
    ],
    [
        # THROWN = 8
        WEAPON_NONE,
        (4, 0, "手雷"),
        (5, 0, "燃烧瓶"),
    ],
]


VEHICLE_LIST = (
    ("ADMIRAL", 0x4B5C5320),
    ("AIRTUG", 0x5D0AAC8F),
    ("AMBULANCE", 0x45D56ADA),
    ("BANSHEE", 0xC1E908D2),
    ("BENSON", 0x7A61B330),
    ("BIFF", 0x32B91AE8),
    ("BLISTA", 0xEB70965F),
    ("BOBCAT", 0x4020325C),
    ("BOXVILLE", 0x898ECCEA),
    ("BUCCANEER", 0xD756460C),
    ("BURRITO", 0xAFBB2CA4),
    ("BURRITO2", 0xC9E8FF76),
    ("BUS", 0xD577C962),
    ("CABBY", 0x705A3E41),
    ("CAVALCADE", 0x779F23AA),
    ("CHAVOS", 0xFBFD5B62),
    ("COGNOSCENTI", 0x86FE0B60),
    ("COMET", 0x3F637729),
    ("COQUETTE", 0x067BC037),
    ("DF8", 0x09B56631),
    ("DILETTANTE", 0xBC993509),
    ("DUKES", 0x2B26F456),
    ("E109", 0x8A765902),
    ("EMPEROR", 0xD7278283),
    ("EMPEROR2", 0x8FC3AADC),
    ("ESPERANTO", 0xEF7ED55D),
    ("FACTION", 0x81A9CDDF),
    ("FBI", 0x432EA949),
    ("FELTZER", 0xBE9075F1),
    ("FEROCI", 0x3A196CEA),
    ("FEROCI2", 0x3D285C4A),
    ("FIRETRUK", 0x73920F8E),
    ("FLATBED", 0x50B0215A),
    ("FORTUNE", 0x255FC509),
    ("FORKLIFT", 0x58E49664),
    ("FUTO", 0x7836CE2F),
    ("FXT", 0x28420460),
    ("HABANERO", 0x34B7390F),
    ("HAKUMAI", 0xEB9F21D3),
    ("HUNTLEY", 0x1D06D681),
    ("INFERNUS", 0x18F25AC7),
    ("INGOT", 0xB3206692),
    ("INTRUDER", 0x34DD8AA1),
    ("LANDSTALKER", 0x4BA4E8DC),
    ("LOKUS", 0xFDCAF758),
    ("MANANA", 0x81634188),
    ("MARBELLA", 0x4DC293EA),
    ("MERIT", 0xB4D8797E),
    ("MINIVAN", 0xED7EADA4),
    ("MOONBEAM", 0x1F52A43F),
    ("MRTASTY", 0x22C16A2F),
    ("MULE", 0x35ED670B),
    ("NOOSE", 0x08DE2A8B),
    ("NSTOCKADE", 0x71EF6313),
    ("ORACLE", 0x506434F6),
    ("PACKER", 0x21EEE87D),
    ("PATRIOT", 0xCFCFEB3B),
    ("PERENNIAL", 0x84282613),
    ("PERENNIAL2", 0xA1363020),
    ("PEYOTE", 0x6D19CCBC),
    ("PHANTOM", 0x809AA4CB),
    ("PINNACLE", 0x07D10BDC),
    ("PMP600", 0x5208A519),
    ("POLICE", 0x79FBB0C5),
    ("POLICE2", 0x9F05F101),
    ("POLPATRIOT", 0xEB221FC2),
    ("PONY", 0xF8DE29A8),
    ("PREMIER", 0x8FB66F9B),
    ("PRES", 0x8B0D2BA6),
    ("PRIMO", 0xBB6B404F),
    ("PSTOCKADE", 0x8EB78F5A),
    ("RANCHER", 0x52DB01E0),
    ("REBLA", 0x04F48FC4),
    ("RIPLEY", 0xCD935EF9),
    ("ROMERO", 0x2560B2FC),
    ("ROM", 0x8CD0264C),
    ("RUINER", 0xF26CEFF9),
    ("SABRE", 0xE53C7459),
    ("SABRE2", 0x4B5D021E),
    ("SABREGT", 0x9B909C94),
    ("SCHAFTER", 0xECC96C3F),
    ("SENTINEL", 0x50732C82),
    ("SOLAIR", 0x50249008),
    ("SPEEDO", 0xCFB3870C),
    ("STALION", 0x72A4C31E),
    ("STEED", 0x63FFE6EC),
    ("STOCKADE", 0x6827CF72),
    ("STRATUM", 0x66B4FC45),
    ("STRETCH", 0x8B13F083),
    ("SULTAN", 0x39DA2754),
    ("SULTANRS", 0xEE6024BC),
    ("SUPERGT", 0x6C9962A9),
    ("TAXI", 0xC703DB5F),
    ("TAXI2", 0x480DAF95),
    ("TRASH", 0x72435A19),
    ("TURISMO", 0x8EF34547),
    ("URANUS", 0x5B73F5B7),
    ("VIGERO", 0xCEC6B9B7),
    ("VIGERO2", 0x973141FC),
    ("VINCENT", 0xDD3BD501),
    ("VIRGO", 0xE2504942),
    ("VOODOO", 0x779B4F2D),
    ("WASHINGTON", 0x69F06B57),
    ("WILLARD", 0x737DAEC2),
    ("YANKEE", 0xBE6FF06A),
    ("BOBBER", 0x92E56A2C),
    ("FAGGIO", 0x9229E4EB),
    ("HELLFURY", 0x22DC8E7F),
    ("NRG900", 0x47B9138A),
    ("PCJ", 0xC9CEAF06),
    ("SANCHEZ", 0x2EF89E46),
    ("ZOMBIEB", 0xDE05FB87),
    ("ANNIHILATOR", 0x31F0B376),
    ("MAVERICK", 0x9D0450CA),
    ("POLMAV", 0x1517D4D9),
    ("TOURMAV", 0x78D70477),
    ("DINGHY", 0x3D961290),
    ("JETMAX", 0x33581161),
    ("MARQUIS", 0xC1CE1183),
    ("PREDATOR", 0xE2E7D4AB),
    ("REEFER", 0x68E27CB6),
    ("SQUALO", 0x17DF5EC2),
    ("TUGA", 0x3F724E66),
    ("TROPIC", 0x1149422F),
    ("CABLECAR", 0xC6C3242D),
    ("SUBWAY_LO", 0x2FBC4D30),
    ("SUBWAY_HI", 0x8B887FDB),
)

COLOR_LIST = [
    0x0A0A0A, 0x252527, 0x656A79, 0x58595A, 0x9CA1A3, 0x96918C, 0x515459, 0x3F3E45,
    0xA5A9A7, 0x979592, 0x767B7C, 0x5A5752, 0xADB0B0, 0x848988, 0x949D9F, 0xA4A7A5, 0x585853, 0xA4A096, 
    0xAFB1B1, 0x6D6C6E, 0x64686A, 0x525661, 0x8C929A, 0x5B5D5E, 0xBDBEC6, 0xB6B6B6, 0x646464, 0xE20606, 
    0x960800, 0x6B0000, 0x611009, 0x4A0A0A, 0x730B0B, 0x570707, 0x260306, 0x9E0000, 0x140002, 0x0F0404, 
    0x0F080A, 0x39191D, 0x552725, 0x4C2929, 0x741D28, 0x6D2837, 0x730A27, 0x640D1B, 0x620B1C, 0x731827, 
    0xAB988F, 0x20202C, 0x44624F, 0x2E5B20, 0x1E2E32, 0x304F45, 0x4D6268, 0x5E7072, 0x193826, 0x2D3A35, 
    0x335F3F, 0x47783C, 0x93A396, 0x9AA790, 0x263739, 0x4C75B7, 0x46597A, 0x5D7E8D, 0x3B4E78, 0x3D4A68, 
    0x6D7A88, 0x162248, 0x272F4B, 0x4E6881, 0x6A7A8C, 0x6F8297, 0x0E316D, 0x395A83, 0x204B6B, 0x2B3E57, 
    0x364155, 0x6C8495, 0x4D5D60, 0x406C8F, 0x134573, 0x105082, 0x385694, 0x001C32, 0x596E87, 0x223457, 
    0x20202C, 0xF5890F, 0x917347, 0x8E8C46, 0xAAAD8E, 0xAE9B7F, 0x96816C, 0x7A7560, 0x9D9872, 0x989586, 
    0x9C8D71, 0x691E3B, 0x722A3F, 0x7C1B44, 0x221918, 0x7F6956, 0x473532, 0x695853, 0x624428, 0x7D6256, 
    0xAA9D84, 0x7B715E, 0xAB9276, 0x635C5A, 0xC9C9C9, 0xD6DAD6, 0x9F9D94, 0x93A396, 0x9C9C98, 0xA7A28F, 
    0x0F6A89, 0xA19983, 0xA3ADC6, 0x9B8B80, 0x8494AB, 0x9EA4AB, 0x86446E, 0xE20606, 0x47783C, 0xD78E10, 
    0x2A77A1, 0x421F21, 0x6F675F, 0xFC2600, 0xFC6D00, 0xFFFFFF
]

COLOR_NAME_LIST = [
    "Black", "BlackPoly", "ConcordBluePoly", "PewterGrayPoly", "SilverStonePoly",
    "WinningSilverPoly", "SteelGrayPoly", "ShadowSilverPoly", "SilverStonePoly2", "PorcelainSilverPoly", "GrayPoly",
    "AnthraciteGrayPoly", "AstraSilverPoly", "AscotGray", "ClearCrystalBlueFrostPoly", "SilverPoly", "DarkTitaniumPoly", 
    "TitaniumFrostPoly", "PoliceWhite", "MediumGrayPoly", "MediumGrayPoly2", "SteelGrayPoly2", "SlateGray",
    "GunMetalPoly", "LightBlueGrey", "SecuricorLightGray", "ArcticWhite", "VeryRed", "TorinoRedPearl", "FormulaRed",
    "BlazeRed", "GracefulRedMica", "GarnetRedPoly", "DesertRed", "CabernetRedPoly", "TurismoRed", "DesertRed2",
    "CurrantRedSolid", "CurrantRedPoly", "ElectricCurrantRedPoly", "MediumCabernetSolid", "WildStrawberryPoly",
    "MediumRedSolid", "BrightRed", "BrightRed2", "MediumGarnetRedPoly", "BrilliantRedPoly", "BrilliantRedPoly2",
    "AlabasterSolid", "TwilightBluePoly", "TorchRed", "Green", "DeepJewelGreen", "AgateGreen", "PetrolBlueGreenPoly",
    "Hoods", "Green2", "DarkGreenPoly", "RioRed", "SecuricorDarkGreen", "SeafoamPoly", "PastelAlabasterSolid",
    "MidnightBlue", "StrikingBlue", "SaxonyBluePoly", "JasperGreenPoly", "MarinerBlue", "HarborBluePoly",
    "DiamondBluePoly", "SurfBlue", "NauticalBluePoly", "LightCrystalBluePoly", "MedRegattaBluePoly", "SpinnakerBlueSolid",
    "UltraBluePoly", "BrightBluePoly", "NassauBluePoly", "MediumSapphireBluePoly", "SteelBluePoly",
    "LightSapphireBluePoly", "MalachitePoly", "MediumMauiBluePoly", "BrightBluePoly2", "BrightBluePoly3", "Blue",
    "DarkSapphireBluePoly", "LightSapphireBluePoly2", "MediumSapphireBlueFiremist", "TwilightBluePoly2", "TaxiYellow",
    "RaceYellowSolid", "PastelAlabaster", "OxfordWhiteSolid", "Flax", "MediumFlax", "PuebloBeige", "LightIvory",
    "SmokeSilverPoly", "BisqueFrostPoly", "ClassicRed", "VermilionSolid", "VermillionSolid", "BistonBrownPoly",
    "LightBeechwoodPoly", "DarkBeechwoodPoly", "DarkSablePoly", "MediumBeechwoodPoly", "WoodrosePoly", "SandalwoodFrostPoly",
    "MediumSandalwoodPoly", "CopperBeige", "WarmGreyMica", "White", "FrostWhite", "HoneyBeigePoly", "SeafoamPoly2",
    "LightTitaniumPoly", "LightChampagnePoly", "ArcticPearl", "LightDriftwoodPoly", "WhiteDiamondPearl", "AntelopeBeige",
    "CurrantBluePoly", "CrystalBluePoly", "TempleCurtainPurple", "CherryRed", "SecuricorDarkGreen2", "TaxiYellow2",
    "PoliceCarBlue", "MellowBurgundy", "DesertTaupePoly", "LammyOrange", "LammyYellow", "VeryWhite"
]