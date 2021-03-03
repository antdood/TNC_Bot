import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import re
from db import db
from members import hasAllMembers, getAllNicks

def isDiscTag(string):
    return re.search("^<@!\d+>$", string)

def isMemberShift(string):
    regex = f'(?i)^({"|".join(getAllNicks())})[+-]\d*$'
    return re.search(regex, string)

def discTagToID(tag):
    return tag[3:-1] # Could user discord's converter here but why? Non critical stuff

async def showRanking(id, channel):
    await channel.send(db.getRankings(id))
    return

load_dotenv()

TOKEN = os.getenv("discord_token")
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Logged in.")
    db()

@bot.command()
async def ranking(msg, *args):

    if(not args):
        await showRanking(msg.author.id, msg.channel)

    elif(len(args) == 1 and isDiscTag(args[0])):
        await showRanking(discTagToID(args[0]), msg.channel)

    elif(len(args) == 9 and hasAllMembers(args)):
        db.newRankings(msg.author.id, args)
      
    elif(all(map(lambda x : isMemberShift(x), args))):
        for a in args:
            # No need for validation here as that's done in isMemberShift
            nick = re.findall("^\w+", a)[0]
            operation = re.findall("[+-]", a)[0]
            amount = int(re.findall("(?<=[+-])\d*", a)[0] or 1)

            db.shiftRanking(msg.author.id, nick, operation, amount)

    else:
        await msg.channel.send("The fuck you trying to do mate")

bot.run(TOKEN)
