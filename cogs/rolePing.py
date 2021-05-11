import discord
import os
import asyncio
from discord.ext import commands


class RolePing(commands.Cog):

    def __init__(self, client):
        self.client = client

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
        f = open("answers.txt", "w", encoding='utf-8')
        if message.mention_everyone:
            members = message.guild.members
        else:
            role_mention = message.role_mentions
            members = role_mention[0].members
        
        #task for event loop
        async def message_member(member, ctx, message, content, answers):

            def message_check(message):
                return message.channel.type == discord.ChannelType.private and message.author == member

            if member != message.author and member != self.client.user:
                await member.send(content + " - von " + message.author.name)
                try: 
                    response = await self.client.wait_for('message', timeout= 60.0, check=message_check)
                    if response:
                        answers.write(response.content + " - " + member.name + '\n')
                except asyncio.TimeoutError:
                    answers.write("Keine Antwort - " + member.name)
                    await member.send("Ja, egal hat sich erledigt")
        
        #Use Event Loop instead of threats
        #wait for every task to finish before continuing
        await asyncio.wait([asyncio.ensure_future(message_member(member, ctx, message, content, f)) for member in members])
        f.close()
        await ctx.send(file=discord.File("answers.txt"))
        os.remove("answers.txt")

def setup(client):
    client.add_cog(RolePing(client))
