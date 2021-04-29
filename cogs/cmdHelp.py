import asyncio,discord,os,random
from discord.ext import commands, tasks
from itertools import cycle

class cmdHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["도움", "도움말", "help"])
    async def cmdHelp(self, ctx):
        embed=discord.Embed(title=f"플레이봇에 관한 도움말 입니다.", description=f"**명령어** 및 **사용법** 등에 대한 설명들이 적혀 있습니다.", color=0xffffff)
        embed.set_author(name="「  PlayBot 도움말  」", icon_url="https://cdn.discordapp.com/avatars/835763308509396993/ea999c4a1977e89642a1d520622e288f.png?size=128")
        embed.add_field(name="도움말 열기", value="`ㅍ도움`, `ㅍhelp`")
        embed.add_field(name="코인 가격 목록", value="`ㅍ코인`, `ㅍ가격`, `ㅍcoin`")
        embed.add_field(name="계좌 정보", value="`ㅍ지갑`, `ㅍ돈`, `ㅍwallet`")
        embed.add_field(name="코인 구매", value="`ㅍ구매 [이름] [개수]`, (`ㅍ매수`, `ㅍbuy`)")
        embed.add_field(name="코인 판매", value="`ㅍ판매 [이름] [개수]`, (`ㅍ매도`, `ㅍsell`)")
        embed.add_field(name="일일 보상", value="`ㅍ돈받기`, `ㅍ일일보상`, `ㅍdaily`")
        embed.add_field(name="한강 온도", value="`ㅍ한강`, `ㅍ한강물`")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(cmdHelp(bot))