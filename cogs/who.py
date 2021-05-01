import discord
import os
import checkPerson as cp
from discord.ext import commands

answered = False

class Who(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Fun Feature to troll someone
    @commands.Cog.listener()
    async def on_message(self, message):
        global answered
        if message.author.id == 115483140130078726 and cp.checkPerson(message):
            if not answered:
                await message.channel.send("WER?")
                answered = True
            else:
                await message.channel.send("NEIN wer gefragt hat! HOOOPS")
                answered = False
    
def setup(client):
    client.add_cog(Who(client))