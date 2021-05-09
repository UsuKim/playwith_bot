import asyncio,discord,os,random,psycopg2,requests
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

class cmdSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    guild = [839006569441394689]

    @cog_ext.cog_slash(name="test",description="테스트용 슬래시 커맨드",guild_ids=guild,options=[create_option(name="code47",description="전승엽 47",option_type=3,required=True,choices=[create_choice(name="첫번째",value="47"),create_choice(name="두번째",value="4747")])])
    async def ping(self, ctx: SlashContext, code47: str):
        await ctx.send(content=f"{code47}")

def setup(bot):
    bot.add_cog(cmdSlash(bot))