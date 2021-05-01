import discord
import os
from discord.ext import commands

class RolePing(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Extract content from message for wikipedia Search
    @commands.Cog.listener()
    async def on_message(self, message):
        #role ping feature
        if "@" in message.content:

            test = message.role_mentions
            for role in message.guild.roles:
                if test[0].id == role.id:
                    for member in role.members:
                        if member != self.client.user:
                            await member.send("Hallo")
    
def setup(client):
    client.add_cog(RolePing(client))
