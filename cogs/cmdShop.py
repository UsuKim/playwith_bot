import asyncio,discord,os,random,psycopg2,requests
from discord.ext import commands, tasks

class cmdShop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["상점", "샵", "shop"])
    async def cmdShop(self, ctx, *args):
        l_args = list(args)
        l_args.append(None)
        if l_args[0] == None or l_args[0] == "목록":
            embed=discord.Embed(title="상점 목록",color=0x8be653)
            embed.add_field(name="낚시상점", value="각종 낚시 용품들을 팝니다.\n`ㅍ상점 낚시`")
            await ctx.send(embed=embed)
        elif l_args[0] == "낚시" or l_args[0] == "낚시상점":
            page1 = {1:"1. <:low_fishinglod:842314659619930113> 하급 낚싯대",2:"2. <:normal_worm:842316324838572062> 일반 미끼"}
            des = ""
            for i in range(len(page1)):
                des += f"page1[i+1]\n"
            embed=discord.Embed(title="낚시 상점",description=des,color=0x3a94ce)
            embed.set_footer(text='페이지 1')
            shop = await ctx.send(embed=embed)
            await shop.add_reaction(":one:")


def setup(bot):
    bot.add_cog(cmdShop(bot))