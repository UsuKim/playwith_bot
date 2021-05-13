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
            page1 = [["하급 낚싯대",100000,"<:low_fishinglod:842314659619930113>",100],["일반 미끼",500,"<:normal_worm:842316324838572062>",0]]
            numbers = {"❌":None,"1️⃣":0,"2️⃣":1}
            des = ""
            num = 0
            for i in page1:
                dur = ''
                num += 1
                if i[3] != 0:
                    dur = f'({i[3]})'
                des += f"{num}. {i[2]} {i[0]}{dur} | {format(i[1],',')} ₩\n"
            embed=discord.Embed(title="낚시 상점",description=des,color=0x3a94ce)
            embed.set_footer(text='페이지 1')
            shop = await ctx.send(embed=embed)
            await shop.add_reaction("1️⃣")
            await shop.add_reaction("2️⃣")
            await shop.add_reaction("❌")

            def check(react, user):
                return user == ctx.author and str(react.emoji) in ['1️⃣', '2️⃣', '❌']
            
            try:
                react, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
            except asyncio.TimeoutError:
                embed.set_footer(text='(시간 만료)')
            else:
                self.bot.cur.execute("SELECT * FROM user_data WHERE id = %s", (str(ctx.author.id),))
                data = self.bot.cur.fetchone()
                if numbers[react.emoji] == None:
                    embed.set_footer(text='(결제 취소)')
                elif page1[numbers[react.emoji]][3] == 0:
                    def worm(m):
                        return m.author == ctx.author and m.channel == ctx.channel
                        
                    try:
                        embed2=discord.Embed(title='구매할 수량을 입력해 주세요.',description='예)\n```10```',color=0x8be653)
                        embed2.set_footer(text="제한시간: 10초")
                        buy = await ctx.send(embed=embed2)
                        msg = await self.bot.wait_for('message', timeout=10.0, check=worm)
                    except asyncio.TimeoutError:
                        embed.set_footer(text='(시간 만료)')
                    else:
                        amount = int(msg)
                        print(amount)
                        if amount <= 0:
                            embed2=discord.Embed(title='구매 수량이 올바르지 않습니다.',description='예)\n```10```',color=0xb40000)
                            embed.set_footer(text='(결제 취소)')
                            await ctx.send(embed=embed2)
                        elif page1[numbers[react.emoji]][1] * amount > data[1]:
                            embed2=discord.Embed(title='잔액이 부족합니다.',description=f'```구매 금액: {format(page1[numbers[react.emoji]][1],",")} ₩\n잔여 금액: {format(data[1],",")} ₩```',color=0xb40000)
                            embed.set_footer(text='(결제 취소)')
                            await ctx.send(embed=embed2)
                        else:
                            money = data[1] - (page1[numbers[react.emoji]][1] * amount)
                            self.bot.cur.execute("UPDATE user_data SET money = %s WHERE id = %s",(money, str(ctx.author.id)))
                            self.bot.cur.execute("UPDATE user_data SET normal_worm = %s WHERE id = %s",(amount, str(ctx.author.id)))
                            embed2=discord.Embed(title='구매 완료',description=f'{page1[numbers[react.emoji]][2]} {page1[numbers[react.emoji]][0]}\n```구매 수량: {amount}개\n보유 수량: {data[21]}개\n구매 금액: {format(page1[numbers[react.emoji]][1] * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)
                            embed.set_footer(text='(결제 성공)')
                            try:
                                await buy.edit(embed=embed2)
                            except:
                                await ctx.send(embed=embed2)
                else:
                    if data[20] >= 1:
                        embed2=discord.Embed(title='낚싯대는 최대 한 개 까지만 소유 가능합니다.',color=0xb40000)
                        embed.set_footer(text='(결제 취소)')
                        await ctx.send(embed=embed2)
                    elif page1[numbers[react.emoji]][1] > data[1]:
                        embed2=discord.Embed(title='잔액이 부족합니다.',description=f'```구매 금액: {format(page1[numbers[react.emoji]][1],",")} ₩\n잔여 금액: {format(data[1],",")} ₩```',color=0xb40000)
                        embed.set_footer(text='(결제 취소)')
                        await ctx.send(embed=embed2)
                    else:
                        money = data[1] - page1[numbers[react.emoji]][1]
                        self.bot.cur.execute("UPDATE user_data SET money = %s WHERE id = %s",(money, str(ctx.author.id)))
                        self.bot.cur.execute("UPDATE user_data SET fishingrod = %s WHERE id = %s",(page1[numbers[react.emoji]][3], str(ctx.author.id)))
                        embed2=discord.Embed(title='구매 완료',description=f'{page1[numbers[react.emoji]][2]} {page1[numbers[react.emoji]][0]}\n```구매 금액: {format(page1[numbers[react.emoji]][1],",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)
                        embed.set_footer(text='(결제 성공)')
                        await ctx.send(embed=embed2)
                try:
                    await shop.edit(embed=embed)
                except:
                    await ctx.send(embed=embed)
                self.bot.conn.commit()


def setup(bot):
    bot.add_cog(cmdShop(bot))