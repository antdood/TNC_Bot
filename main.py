import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import re
from db import db
from members import hasAllMembers, getAllNicks
from pathlib import Path

def getFile(path, mode = "r"):
    cdir = Path(__file__).resolve().parent

    return open(cdir / path, mode)

def isDiscTag(string):
    return re.search("^<@!?\d+>$", string)

def isMemberShift(string):
    regex = f'(?i)^({"|".join(getAllNicks())})[+-]\d*$'
    return re.search(regex, string)

def discTagToID(tag):
    # Could user discord's converter here but why? Non critical stuff + would need to await for stuff
    charsToBeRemoved = ["<", "@", "!", ">"]

    for c in charsToBeRemoved:
        tag = tag.replace(c, "")

    return tag

async def showRanking(user, channel):
    rankings = db.getRankings(user.id)
    
    if rankings:
        with getFile("templates/rankingMain.md") as mainFile, getFile("templates/list.md") as listFile:
            mainTemplate = mainFile.read()
            listTemplate = listFile.read()

        displayName = user.nick or user.name

        text = mainTemplate.format(header = f"__Rankings of **{displayName}**__", list = listTemplate.format(rankings))

        await channel.send(text)
    else:
        await channel.send(f"**{displayName}** has yet to set their rankings")
    return

load_dotenv()

TOKEN = os.getenv("discord_token")
bot = commands.Bot(command_prefix="!", help_command=None)

@bot.event
async def on_ready():
    print("Logged in.")
    db()

@bot.command(aliases = ['rankings'])
async def ranking(msg, *args):

    if(not args):
        await showRanking(msg.author, msg.channel)

    elif(len(args) == 1 and isDiscTag(args[0])):
        for user in msg.message.mentions:
            print(user)
            print(user.id)
            await showRanking(user, msg.channel)

    elif(len(args) == 9 and hasAllMembers(args)):
        db.newRankings(msg.author.id, args)
        await showRanking(msg.author, msg.channel)
      
    elif(all(map(lambda x : isMemberShift(x), args))):
        if(db.userHasRankings(msg.author.id)):
            for a in args:
                # No need for validation here as that's done in isMemberShift
                nick = re.findall("^\w+", a)[0]
                operation = re.findall("[+-]", a)[0]
                amount = int(re.findall("(?<=[+-])\d*", a)[0] or 1)

                db.shiftRanking(msg.author.id, nick, operation, amount)
            await showRanking(msg.author, msg.channel)
        else:
            await msg.channel.send("Please set your initial rankings before trying to change them. !help for more info.")

    else:
        await msg.channel.send("The fuck you trying to do mate")

@bot.command()
async def help(context):
    with getFile("templates/help.md") as f:
        await context.channel.send(f.read())

@bot.command(aliases = ['credit'])
async def credits(context):
    with getFile("templates/credits.md") as f:
        await context.channel.send(f.read().format("<@158010930200838144>"))

bot.run(TOKEN)
