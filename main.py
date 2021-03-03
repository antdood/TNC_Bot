import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import re
from db import db
from members import hasAllMembers

def isDiscTag(string):
    return re.search("^<@!\d+>$", string)

def discTagToID(tag):
    return tag[3:-1] # Could user discord's converter here but why? Non critical stuff

async def showRanking(id, channel):
    print(db.getRankings(id))

    await channel.send(db.getRankings(id))

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

    if(len(args) == 1 and isDiscTag(args[0])):
        await showRanking(discTagToID(args[0]), msg.channel)

    if(len(args) == 9 and hasAllMembers(args)):
        db.newRankings(msg.author.id, args)
        

bot.run(TOKEN)
