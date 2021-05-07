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
            if bat < 500:
                embed=discord.Embed(title="금액이 너무 작습니다.",description='```최소 금액 : 500 ₩```',color=0xb40000)
                await ctx.send(embed=embed)
            elif bat > data[1]:
                embed=discord.Embed(title="금액이 너무 큽니다.",description=f'```잔여 금액 : {format(data[1], ",")} ₩```',color=0xb40000)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'**{format(bat, ",")} ₩** 을 걸었습니다!')
                message = await ctx.send('<a:slot_ing:840071330803351554> <a:slot_ing:840071330803351554> <a:slot_ing:840071330803351554>')
                await asyncio.sleep(3)
                slots = {'play':0.03,'dia':0.05,'star':0.08,'bell':0.12,'clov':0.17,'lemon':0.23,'cher':0.32}
                slot1_r = random.random()*100
                if 0.0 <= slot1_r < 3.0:
                    slot1_r = 'play'
                    slot1 = self.bot.get_emoji(840069371028176896)
                elif 3.0 <= slot1_r < 8.0:
                    slot1_r = 'dia'
                    slot1 = self.bot.get_emoji(840054615122771968)
                elif 8.0 <= slot1_r < 16.0:
                    slot1_r = 'star'
                    slot1 = self.bot.get_emoji(840053608753922128)
                elif 16.0 <= slot1_r < 28.0:
                    slot1_r = 'bell'
                    slot1 = self.bot.get_emoji(840052403575455775)
                elif 28.0 <= slot1_r < 45.0:
                    slot1_r = 'clov'
                    slot1 = self.bot.get_emoji(840052106530783302)
                elif 45.0 <= slot1_r < 68.0:
                    slot1_r = 'lemon'
                    slot1 = self.bot.get_emoji(840051770939801640)
                elif 68.0 <= slot1_r < 100.0:
                    slot1_r = 'cher'
                    slot1 = self.bot.get_emoji(840051236371038208)

                slot2_r = random.random()*100
                if 0.0 <= slot2_r < 3.0:
                    slot2_r = 'play'
                    slot2 = self.bot.get_emoji(840069371028176896)
                elif 3.0 <= slot2_r < 8.0:
                    slot2_r = 'dia'
                    slot2 = self.bot.get_emoji(840054615122771968)
                elif 8.0 <= slot2_r < 16.0:
                    slot2_r = 'star'
                    slot2 = self.bot.get_emoji(840053608753922128)
                elif 16.0 <= slot2_r < 28.0:
                    slot2_r = 'bell'
                    slot2 = self.bot.get_emoji(840052403575455775)
                elif 28.0 <= slot2_r < 45.0:
                    slot2_r = 'clov'
                    slot2 = self.bot.get_emoji(840052106530783302)
                elif 45.0 <= slot2_r < 68.0:
                    slot2_r = 'lemon'
                    slot2 = self.bot.get_emoji(840051770939801640)
                elif 68.0 <= slot2_r < 100.0:
                    slot2_r = 'cher'
                    slot2 = self.bot.get_emoji(840051236371038208)

                slot3_r = random.random()*100
                if 0.0 <= slot3_r < 3.0:
                    slot3_r = 'play'
                    slot3 = self.bot.get_emoji(840069371028176896)
                elif 3.0 <= slot3_r < 8.0:
                    slot3_r = 'dia'
                    slot3 = self.bot.get_emoji(840054615122771968)
                elif 8.0 <= slot3_r < 16.0:
                    slot3_r = 'star'
                    slot3 = self.bot.get_emoji(840053608753922128)
                elif 16.0 <= slot3_r < 28.0:
                    slot3_r = 'bell'
                    slot3 = self.bot.get_emoji(840052403575455775)
                elif 28.0 <= slot3_r < 45.0:
                    slot3_r = 'clov'
                    slot3 = self.bot.get_emoji(840052106530783302)
                elif 45.0 <= slot3_r < 68.0:
                    slot3_r = 'lemon'
                    slot3 = self.bot.get_emoji(840051770939801640)
                elif 68.0 <= slot3_r < 100.0:
                    slot3_r = 'cher'
                    slot3 = self.bot.get_emoji(840051236371038208)
                
                if slot1_r == slot2_r == slot3_r:
                    money = data[1] - bat + round((1/(25*slots[slot1_r]*slots[slot2_r]*slots[slot3_r])*bat))
                elif [slot1_r,slot2_r,slot3_r].count('play') == 1:
                    l = [slot1_r,slot2_r,slot3_r].remove('play')
                    if l[0] == l[1]:
                        money = data[1] - bat + round((1/(25*slots[slot1_r]*slots[slot2_r]*slots[slot3_r]*3)*bat))
                    else:
                        money = data[1] - bat
                elif [slot1_r,slot2_r,slot3_r].count('dia') == 1:
                    l = [slot1_r,slot2_r,slot3_r].remove('dia')
                    if l[0] == l[1]:
                        money = data[1] - bat + round((1/(25*slots[slot1_r]*slots[slot2_r]*slots[slot3_r]*3)*bat))
                    else:
                        money = data[1] - bat
                elif [slot1_r,slot2_r,slot3_r].count('star') == 1:
                    l = [slot1_r,slot2_r,slot3_r].remove('star')
                    if l[0] == l[1]:
                        money = data[1] - bat + round((1/(25*slots[slot1_r]*slots[slot2_r]*slots[slot3_r]*3)*bat))
                    else:
                        money = data[1] - bat
                else:
                    money = data[1] - bat
                cur.execute("UPDATE user_data SET money = %s WHERE id = %s",(money, str(ctx.author.id)))
                await message.edit(content=f"{slot1}{slot2}{slot3}")
                embed=discord.Embed(title='슬롯머신 결과',description=f'```손익: {format(money-data[1],",")} ₩\n잔액: {money} ₩```')
                await ctx.send(embed=embed)
            conn.commit()
            conn.close()

def setup(bot):
    bot.add_cog(cmdSlot(bot))