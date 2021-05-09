import asyncio,discord,os,random,psycopg2,requests
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

class cmdSlashCoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    guild = [839006569441394689]

    @cog_ext.cog_slash(name="test",description="테스트용 슬래시 커맨드",guild_ids=guild,options=[create_option(name="code47",description="전승엽 47",option_type=3,required=True,choices=[create_choice(name="첫번째",value="47"),create_choice(name="두번째",value="4747")])])
    async def ping(self, ctx: SlashContext, code47: str):
        await ctx.send(content=f"{code47}")
    
    @cog_ext.cog_slash(name=["시세", "가격"],description="코인의 시세를 확인합니다.",guild_ids=guild)
    async def cmdSlashCoin(self, ctx: SlashContext):
        if self.bot.r_btc < 0:
            ar_btc = '▼'
            pm_btc = '-'
        elif self.bot.r_btc > 0:
            ar_btc = '▲'
            pm_btc = '+'
        else:
            ar_btc = '■'
            pm_btc = '='
        
        if self.bot.r_eth < 0:
            ar_eth = '▼'
            pm_eth = '-'
        elif self.bot.r_eth > 0:
            ar_eth = '▲'
            pm_eth = '+'
        else:
            ar_eth = '■'
            pm_eth = '='
        
        if self.bot.r_ltc < 0:
            ar_ltc = '▼'
            pm_ltc = '-'
        elif self.bot.r_ltc > 0:
            ar_ltc = '▲'
            pm_ltc = '+'
        else:
            ar_ltc = '■'
            pm_ltc = '='
        
        if self.bot.r_dot < 0:
            ar_dot = '▼'
            pm_dot = '-'
        elif self.bot.r_dot > 0:
            ar_dot = '▲'
            pm_dot = '+'
        else:
            ar_dot = '■'
            pm_dot = '='
        
        if self.bot.r_ada < 0:
            ar_ada = '▼'
            pm_ada = '-'
        elif self.bot.r_ada > 0:
            ar_ada = '▲'
            pm_ada = '+'
        else:
            ar_ada = '■'
            pm_ada = '='
        
        if self.bot.r_doge < 0:
            ar_doge = '▼'
            pm_doge = '-'
        elif self.bot.r_doge > 0:
            ar_doge = '▲'
            pm_doge = '+'
        else:
            ar_doge = '■'
            pm_doge = '='
        
        if self.bot.r_xrp < 0:
            ar_xrp = '▼'
            pm_xrp = '-'
        elif self.bot.r_xrp > 0:
            ar_xrp = '▲'
            pm_xrp = '+'
        else:
            ar_xrp = '■'
            pm_xrp = '='
        
        if self.bot.r_trx < 0:
            ar_trx = '▼'
            pm_trx = '-'
        elif self.bot.r_trx > 0:
            ar_trx = '▲'
            pm_trx = '+'
        else:
            ar_trx = '■'
            pm_trx = '='
        description = '```diff\n'
        description += f'{pm_btc} 비트코인　: {format(self.bot.n_btc,",")} ₩ ({ar_btc} {format(self.bot.r_btc,",")} ₩)\n'
        description += f'{pm_eth} 이더리움　: {format(self.bot.n_eth,",")} ₩ ({ar_eth} {format(self.bot.r_eth,",")} ₩)\n'
        description += f'{pm_ltc} 라이트코인: {format(self.bot.n_ltc,",")} ₩ ({ar_ltc} {format(self.bot.r_ltc,",")} ₩)\n'
        description += f'{pm_dot} 폴카닷　　: {format(self.bot.n_dot,",")} ₩ ({ar_dot} {format(self.bot.r_dot,",")} ₩)\n'
        description += f'{pm_ada} 에이다　　: {format(self.bot.n_ada,",")} ₩ ({ar_ada} {format(self.bot.r_ada,",")} ₩)\n'
        description += f'{pm_doge} 도지코인　: {format(self.bot.n_doge,",")} ₩ ({ar_doge} {format(self.bot.r_doge,",")} ₩)\n'
        description += f'{pm_xrp} 리플　　　: {format(self.bot.n_xrp,",")} ₩ ({ar_xrp} {format(self.bot.r_xrp,",")} ₩)\n'
        description += f'{pm_trx} 트론　　　: {format(self.bot.n_trx,",")} ₩ ({ar_trx} {format(self.bot.r_trx,",")} ₩)'
        description += '```'
        embed=discord.Embed(title=f"현재 시세", description=description, color=0x8be653)
        embed.set_footer(text=f'다음 변동까지 {self.bot.time}초')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(cmdSlashCoin(bot))