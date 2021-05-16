import asyncio,discord,os,random,psycopg2,requests
from cogs.cmdShop import cmdShop
from discord.ext import commands, tasks

class cmdFishing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["낚시", "낚", "fishing", "fish"])
    async def cmdFishing(self, ctx, *args):
        if len(args) != 0:
            if args[0] == '상점':
                await cmdShop(self.bot).cmdShop(self, ctx, '낚시')
        else:
            self.bot.cur.execute("SELECT * FROM user_data WHERE id = %s", (str(ctx.author.id),))
            data = self.bot.cur.fetchone()
            description = ''
            description += f'<:normal_worm:842316324838572062> 일반 미끼: {data[21]}'
            embed=discord.Embed(title='미끼를 선택해 주세요.',description=description,color=0x8be653)
            worms = await ctx.send(embed=embed)
            normal = self.bot.get_emoji(842316324838572062)
            await worms.add_reaction(normal)

def setup(bot):
    bot.add_cog(cmdFishing(bot))