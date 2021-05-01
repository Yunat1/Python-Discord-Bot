import discord
from discord.ext import commands
import os
import sys, traceback
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='$', intents=intents)

if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
    
@client.event
async def on_ready():
    print(f'\n\nLogged in as: {client.user.name} - {client.user.id}\nVersion: {discord.__version__}\n')

client.run(TOKEN, bot=True, reconnect=True)

