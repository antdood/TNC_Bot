from db import db
from collections import defaultdict

def generateGlobalRankingText(mode = "default"):
    rankingDistribution = db.getRankingDistribution()
    memberScores = getMemberScores(rankingDistribution)

    messages = []

    if(mode == "default"):
        text = f"__**Global Rankings**__\n\n"
        for i, m in enumerate(memberScores):
            text += f"{i+1}. {m} with a score of {memberScores[m]}\n"
        messages.append(text)

    elif(mode == "average"):
        text = "\n__**Average Rankings**__\n"

        averages = getAverageRankings(rankingDistribution)

        for m in averages:
            text += f"{averages[m]:.2f}. {m}\n"

        messages.append(text)

    elif(mode == "full"):
        text = "\n__**Full Stats**__\n\n"

        rankCounts = getRankCounts(rankingDistribution)
        averages = getAverageRankings(rankingDistribution)

        for member in rankCounts:
            text += f"__**{member}**__\n\n"
            text += f"Average Rank __**{averages[member]:.2f}**__\n"

            for rank in range(1,10):
                if(rankCounts[member][rank] == 0):
                    continue
                text += f"Best Rank :heart:**{rank}**:heart: __{rankCounts[member][rank]}__ times\n"
                break

            for rank in reversed(range(1,10)):
                if(rankCounts[member][rank] == 0):
                    continue
                text += f"Worst Rank :broken_heart:**{rank}**:broken_heart: __{rankCounts[member][rank]}__ times\n"
                break

            text += "\n"

            for rank in range(1,10):
                text += f"Ranked **{rank}**:medal: {rankCounts[member][rank]} times\n"
            
            messages.append(text)
            text = ""

    else:
        # Sadly this will never trigger. Too many checks before this point :sob:
        messages.append("The only stat you're getting is of your complete fucking inability to follow simple intructions you imbecile. Go read a book.")

    return messages

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

def getRankCounts(rankingDistribution = None, sort = True):
    if(not rankingDistribution):
        rankingDistribution = db.getRankingDistribution()

    rankCounts = defaultdict(lambda: defaultdict(int))

    for member, ranking, count in rankingDistribution:
        rankCounts[member][ranking] = count

    if(sort):
        rankCounts = dict(sorted(rankCounts.items(), key = memberAgeSort))

    return rankCounts

def memberAgeSort(member):
    ageSort = {
        "Nayeon" : 1,
        "Jeongyeon" : 2,
        "Momo" : 3,
        "Sana" : 4,
        "Jihyo" : 5,
        "Mina" : 6,
        "Dahyun" : 7,
        "Chaeyoung" : 8,
        "Tzuyu" : 9
    }

    return ageSort[member[0]]
