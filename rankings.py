from db import db
from collections import defaultdict

def generateGlobalRankingText(mode = "default"):
    rankingDistribution = db.getRankingDistribution()
    memberScores = getMemberScores(rankingDistribution)

    text = ""

    if(mode == "default"):
        text = f"__**Global Rankings**__\n\n"
        for i, m in enumerate(memberScores):
            text += f"{i+1}. {m} with a score of {memberScores[m]}\n"

    elif(mode == "average"):
        text = "\n__**Average Rankings**__\n"

        averages = getAverageRankings(rankingDistribution)

        for m in averages:
            text += f"{averages[m]:.2f}. {m}\n"

    elif(mode == "full"):
        text = "\n__**Full Stats**__\n"
        text += "__Individual Stats__\n"

        print(rankingDistribution)
        print({member : {ranking : count} for member, ranking, count in rankingDistribution})



    return text

def getMemberScores(rankingDistribution = None, sort = True):
    # Non linear as more weighting should be placed on higher ranks while scoring flattens on lower ranks.
    rankingScores = {
        1 : 10,
        2 : 7,
        3 : 5,
        4 : 4,
        5 : 3,
        6 : 2,
        7 : 1,
        8 : 0,
        9 : 0
    }

    if(not rankingDistribution):
        rankingDistribution = db.getRankingDistribution()

    memberScores = defaultdict(int)

    for member, ranking, count in rankingDistribution:
        memberScores[member] += (rankingScores[ranking] * count)

    if(sort):
        memberScores = dict(sorted(memberScores.items(), key = lambda member : member[1], reverse = True))

    return memberScores

def getAverageRankings(rankingDistribution = None, sort = True):
    if(not rankingDistribution):
        rankingDistribution = db.getRankingDistribution()

    data = defaultdict(lambda: defaultdict(int))

    for member, ranking, count in rankingDistribution:
        data[member]["total"] += (ranking * count)
        data[member]["count"] += count

    averages = {}
    for member in data:
        averages[member] = data[member]["total"] / data[member]["count"]
    # Or in dict comprehension form
    # averages = {member: (val["total"] / val["count"]) for member, val in data.items()}

    if(sort):
        averages = dict(sorted(averages.items(), key = lambda member : member[1]))

    return averages