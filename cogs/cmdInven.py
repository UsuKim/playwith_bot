import asyncio,discord,os,random,psycopg2,requests
from discord.ext import commands, tasks

class cmdInven(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["인벤토리", "인벤", "가방", "inventory", "inven"])
    async def cmdInven(self, ctx):
        self.bot.cur.execute("SELECT * FROM user_data WHERE id = %s", (str(ctx.author.id),))
        data = self.bot.cur.fetchone()
        fs = {1:'하급 낚싯대'}
        description = ''
        description += f'낚싯대: {fs[data[22]]}({data[20]})'
        embed=discord.Embed(title='인벤토리',description=description,color=0x8be653)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(cmdInven(bot))