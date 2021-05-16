import asyncio,discord,os,random,psycopg2,requests
from cogs.cmdShop import cmdShop
from discord.ext import commands, tasks

class cmdFishing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["낚시", "낚", "fishing", "fish"])
    async def cmdInven(self, ctx, *args):
        if len(args) != 0:
            if args[0] == '상점':
                cmdShop(ctx, '낚시')
        embed=discord.Embed(title='미끼를 선택해 주세요.',color=0x8be653)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(cmdFishing(bot))