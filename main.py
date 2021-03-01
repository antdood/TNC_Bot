import discord
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("discord_token")

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(message.content)

client.run(TOKEN)
