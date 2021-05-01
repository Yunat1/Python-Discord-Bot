import discord
import os
import wikiSearch as search
from discord.ext import commands

class Wiki(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Extract content from message for wikipedia Search
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.content.startswith('!'):

            def check(m):
                num = len(links)
                test = list(range(1, num  + 1))
                try:
                    return int(m.content) in test
                except ValueError:
                    print("Input is not a number. Will be ignored")

            keyword = message.content[1:].replace(' ', '_')
            text, links = search.search_web(keyword)
            await message.channel.send(text)

            if len(text) < 50 and links:
                await message.channel.send(file=discord.File(keyword + ".txt"))
                msg = await self.client.wait_for("message", check = check)
                text, links = search.search_web(links[int(msg.content) - 1])
                await message.channel.send(text)
                os.remove(keyword + ".txt")
    
def setup(client):
    client.add_cog(Wiki(client))


