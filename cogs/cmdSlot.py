import asyncio,discord,os,random,psycopg2
from discord.ext import commands, tasks
from itertools import cycle

class cmdSlot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["슬롯머신", "슬롯", "슬", "slot"])
    async def cmdSlot(self, ctx, *args):
        try:
            bat = int(args[0])
        except:
            embed=discord.Embed(title="금액이 올바르지 않습니다.",description='예)\n```ㅍ슬롯 1000```',color=0xb40000)
            await ctx.send(embed=embed)
        else:
            DATABASE_URL = os.environ['DATABASE_URL']
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            cur.execute("SELECT * FROM user_data WHERE id = %s", (str(ctx.author.id),))
            data = cur.fetchone()
            if bat < 500 or bat > data[1]:
                embed=discord.Embed(title="금액이 올바르지 않습니다.",description='예)\n```ㅍ슬롯 1000```',color=0xb40000)
            else:
                play = self.bot.get_emoji(840069371028176896)
                await ctx.send(f'**{format(bat, ",")} ₩** 을 걸었습니다!')
                message = await ctx.send('<a:slot_ing:840071330803351554> <a:slot_ing:840071330803351554> <a:slot_ing:840071330803351554>')
                await asyncio.sleep(3)
                await message.edit(content=f"{play}{play}{play}")
            conn.commit()
            conn.close()

def setup(bot):
    bot.add_cog(cmdSlot(bot))