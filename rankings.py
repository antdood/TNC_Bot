from db import db
from collections import defaultdict

def generateGlobalRankingText(detailLevel = 0):
    rankingDistribution = db.getRankingDistribution()
    memberScores = getMemberScores(rankingDistribution)

    text = f"__**Global Rankings**__\n\n"

    if(detailLevel == 0):
        for i, member in enumerate(memberScores):
            text += f"{i+1}. {member}\n"

    elif(detailLevel == 1):
        for i, member in enumerate(memberScores):
            text += f"{i+1}. {member} with a score of {memberScores[member]}\n"

    elif(detailLevel == 2):
        for i, member in enumerate(memberScores):
            text += f"{i+1}. {member} with a score of {memberScores[member]}\n"

        text += "\n__**Average Rankings**__"

        getAverageRankings(rankingDistribution)

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

def getAverageRankings(rankingDistribution = None):
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
    averages2 = {member: (val["total"] / val["count"]) for member, val in data.items()}

    print(averages)
    print(averages2)