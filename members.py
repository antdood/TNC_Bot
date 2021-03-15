members = {
    "Nayeon": [
        "NAYEON",
        "나",
        "나연",
        "NA",
        "NAYEONNIE",
        "BUNNY",
        "UNNIE"
        ],
    "Jeongyeon": [
        "JEONGYEON",
        "정",
        "정연",
        "JEONG",
        "JEONGERS"
    ],
    "Momo" : [
        "MOMO",
        "모",
        "모모",
        "MO",
        "MOMORING"
    ],
    "Sana" : [
        "SANA",
        "사",
        "사나",
        "SA"
    ],
    "Jihyo" : [
        "JIHYO",
        "지",
        "지효",
        "JI",
        "LEADER"
    ],
    "Mina" : [
        "MINA",
        "미",
        "미나",
        "MI",
        "PENGUIN",
        "MINARI"
    ],
    "Dahyun" : [
        "DAHYUN",
        "다",
        "다현",
        "DA",
        "DUBU",
        "TOFU"
    ],
    "Chaeyoung" : [
        "CHAEYOUNG",
        "채",
        "채영",
        "CHAE",
        "CUB"
    ],
    "Tzuyu" : [
        "TZUYU",
        "쯔",
        "쯔위",
        "TZU",
        "MAKNAE",
        "CHEWY"
    ]
}

def hasAllMembers(inList):
    return all(map(lambda x : set(x) & set(map(lambda x : x.upper(), inList)), members.values()))

def nickToName(inNick):
    inNick = inNick.upper()
    for name, nicks in members.items():
        for nick in nicks:
            if nick == inNick:
                return name
    return None

def getAllNicks():
    out = []

    for nicks in members.values():
        out += nicks

    return out

def isMember(string):
    if(string.upper() in getAllNicks()):
        return nickToName(string)
    return None