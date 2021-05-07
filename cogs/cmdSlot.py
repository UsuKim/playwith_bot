import asyncio,discord,os,random
from discord.ext import commands, tasks
from itertools import cycle

class cmdSlot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["슬롯머신", "슬롯", "슬", "slot"])
    async def cmdSlot(self, ctx):
        await ctx.send('개발중...')

def setup(bot):
    bot.add_cog(cmdSlot(bot))