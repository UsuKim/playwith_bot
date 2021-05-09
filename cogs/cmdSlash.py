import asyncio,discord,os,random,psycopg2,requests
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext

class cmdSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="ping")
    async def ping(self, ctx: SlashContext):
        await ctx.send(content="Pong!")

def setup(bot):
    bot.add_cog(cmdSlash(bot))