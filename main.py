import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import re
from db import db, getdb

def isDiscTag(string):
    return re.search("^<@!\d+>$", string)

def showRanking(id):
    print(id)

members = {"Nayeon", "Jeongyeon", "Momo", "Sana", "Jihyo", "Mina", "Dahyun", "Chaeyoung", "Tzuyu"}

load_dotenv()

TOKEN = os.getenv("discord_token")
pw = os.getenv("sql_password")

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Logged in.")
    db()

@bot.command()
async def ranking(msg, *args):

    print(args)
    
    print(str(msg.author) + " | " + str(msg.author.id))

    print(await commands.UserConverter().convert(msg, args[0]))

    if(len(args) == 1 and isDiscTag(args[0])):
        showRanking(args[0])

    if(len(args) == 9 and not (set(args)^members)):
        print("redoing rankings")


bot.run(TOKEN)
