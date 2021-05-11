import discord
import os
import asyncio
from discord.ext import commands


class RolePing(commands.Cog):

    def __init__(self, client):
        self.client = client

    #task for event loop
    async def private_message(self, ctx, message, member, content):

        def message_check(message):
            return message.channel.type == discord.ChannelType.private and message.author == member

        await member.send(content + " - von " + message.author.name)
        try: 
            #thread for each user to ask at the same time
            response = await self.client.wait_for('message', timeout= 60.0, check=message_check)
            if response:
                await ctx.send(response.content + " - " + member.name)
        except asyncio.TimeoutError:
            await ctx.send("Keine Antwort - " + member.name)
            await member.send("Ja, egal hat sich erledigt")


    #Extract content from message for wikipedia Search
    @commands.command(name='game')
    async def game(self, ctx):

        #role ping feature
        message = ctx.message
        content = ctx.message.content[6:]

        #extract game from message and remove ping
        if '@everyone' in content:
            content = content.replace('@everyone ', '')
        else:
            index = content.index('<')
            content = content[:index] + content [index + 23:]

        #Dm users with pinged role
        threads = list()
        if message.mention_everyone:
            members = message.guild.members
        else:
            role_mention = message.role_mentions
            members = role_mention[0].members
        for member in members:
            if member != self.client.user:
                #using event loop with task instead of threats
                asyncio.create_task(self.private_message(ctx, message, member, content))

def setup(client):
    client.add_cog(RolePing(client))
