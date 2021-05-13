import asyncio,discord,os,random
from discord.ext import commands, tasks
from itertools import cycle

class cmdHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["도움", "도움말", "명령어", "help"])
    async def cmdHelp(self, ctx):
        embed=discord.Embed(title=f"플레이봇에 관한 도움말 입니다.", description=f"**명령어** 및 **사용법** 등에 대한 설명들이 적혀 있습니다.", color=0xffffff)
        embed.set_author(name="「  PlayBot 도움말  」", icon_url=self.bot.user.avatar_url)
        embed.add_field(name="도움말 열기", value="`ㅍ도움`, `ㅍhelp`")
        embed.add_field(name="코인 가격 목록", value="`ㅍ코인`, `ㅍ가격`, `ㅍcoin`")
        embed.add_field(name="계좌 정보", value="`ㅍ지갑`, `ㅍ돈`, `ㅍwallet`")
        embed.add_field(name="그래프 보기", value="`ㅍ그래프`, `ㅍ그`, `ㅍgraph`")
        embed.add_field(name="코인 매수", value="`ㅍ매수 [이름] [개수]`, (`ㅍ구입`, `ㅍbuy`)")
        embed.add_field(name="코인 매도", value="`ㅍ매도 [이름] [개수]`, (`ㅍ판매`, `ㅍsell`)")
        embed.add_field(name="슬롯머신", value="`ㅍ슬롯머신`, `ㅍ슬롯`, `ㅍslot`")
        embed.add_field(name="일일 보상", value="`ㅍ돈받기`, `ㅍ일일보상`, `ㅍdaily`")
        embed.add_field(name="랭킹 확인", value="`ㅍ랭킹`, `ㅍ순위`, `ㅍrank`")
        embed.add_field(name="한강 온도", value="`ㅍ한강`, `ㅍ한강물`")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(cmdHelp(bot))