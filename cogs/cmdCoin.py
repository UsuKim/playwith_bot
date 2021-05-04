import asyncio,discord,os,random,psycopg2,requests
from upbitpy import Upbitpy
from discord.ext import commands, tasks
from itertools import cycle

class cmdCoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["코인", "가격", "시세", "coin", "price"])
    async def cmdCoin(self, ctx):
        async with ctx.typing():
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
            description = '```diff\n'
            description += f'{pm_btc} 비트코인　: {format(self.bot.n_btc,",")} ₩ ({ar_btc} {format(self.bot.r_btc,",")} ₩)\n'
            description += f'{pm_eth} 이더리움　: {format(self.bot.n_eth,",")} ₩ ({ar_eth} {format(self.bot.r_eth,",")} ₩)\n'
            description += f'{pm_ltc} 라이트코인: {format(self.bot.n_ltc,",")} ₩ ({ar_ltc} {format(self.bot.r_ltc,",")} ₩)\n'
            description += f'{pm_dot} 폴카닷　　: {format(self.bot.n_dot,",")} ₩ ({ar_dot} {format(self.bot.r_dot,",")} ₩)\n'
            description += f'{pm_ada} 에이다　　: {format(self.bot.n_ada,",")} ₩ ({ar_ada} {format(self.bot.r_ada,",")} ₩)\n'
            description += f'{pm_doge} 도지코인　: {format(self.bot.n_doge,",")} ₩ ({ar_doge} {format(self.bot.r_doge,",")} ₩)'
            description += '```'
        embed=discord.Embed(title=f"현재 시세", description=description, color=0x8be653)
        embed.set_footer(text=f'다음 변동까지 {self.bot.time}초')
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["구매", "매수", "구입", "buy"])
    async def cmdBuy(self, ctx, *args):
        try:
            _id = args[0]
            if args[1] == '모두' or args[1] == '전부' or args[1] == 'all':
                _all = True
                amount = 1
            else:
                _all = False
                amount = int(args[1])
        except:
            if len(args) != 2:
                embed=discord.Embed(title="인수의 개수가 올바르지 않습니다.",description='예)\n```ㅍ구매 비트코인 1```',color=0xb40000)
            else:
                embed=discord.Embed(title="구매 수량이 올바르지 않습니다.",description='예)\n```ㅍ구매 비트코인 1```',color=0xb40000)
        else:
            async with ctx.typing():
                DATABASE_URL = os.environ['DATABASE_URL']
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                cur = conn.cursor()
                cur.execute("SELECT * FROM user_data WHERE id = %s", (str(ctx.author.id),))
                data = cur.fetchone()
                if data == None:
                    cur.execute("INSERT INTO user_data VALUES (%s, 100000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)",(str(ctx.author.id),))
                    embed=discord.Embed(title="계좌가 없으시군요! 지금 만들어 드리겠습니다.", description='```계좌 생성 보너스: 100,000 ₩```', color=0x8be653)
                elif len(args) != 2:
                    embed=discord.Embed(title="인수의 개수가 올바르지 않습니다.",description='예)\n```ㅍ구매 비트코인 1```',color=0xb40000)
                elif amount < 1:
                    embed=discord.Embed(title="구매 수량이 올바르지 않습니다.",description='예)\n```ㅍ구매 비트코인 1```',color=0xb40000)
                else:
                    if _id == '비트코인' or _id == 'btc' or _id == '비트':
                        if _all == True:
                            amount = data[1] // self.bot.n_btc
                        if self.bot.n_btc * amount > data[1]:
                            embed=discord.Embed(title='잔액이 부족합니다.',description=f'```구매 금액: {format(self.bot.n_btc * amount,",")} ₩\n잔여 금액: {format(data[1],",")} ₩```',color=0xb40000)
                        elif amount == 0:
                            embed=discord.Embed(title="구매 수량이 올바르지 않습니다.",description='예)\n```ㅍ구매 비트코인 1```',color=0xb40000)
                        else:
                            coin = data[2] + amount
                            cur.execute("UPDATE user_data SET btc = %s WHERE id = %s",(coin, str(ctx.author.id)))
                            money = data[1] - (self.bot.n_btc * amount)
                            cur.execute("UPDATE user_data SET money = %s WHERE id = %s",(money, str(ctx.author.id)))
                            bought = data[8] + (self.bot.n_btc * amount)
                            cur.execute("UPDATE user_data SET b_btc = %s WHERE id = %s",(bought, str(ctx.author.id)))
                            embed=discord.Embed(title='구매 완료',description=f'```구매 수량: {amount}개\n보유 화폐: {coin}개\n구매 금액: {format(self.bot.n_btc * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)

                    elif _id == '이더리움' or _id == 'eth' or _id == '이더':
                        if _all == True:
                            amount = data[1] // self.bot.n_eth
                        if self.bot.n_eth * amount > data[1]:
                            embed=discord.Embed(title='잔액이 부족합니다.',description=f'```구매 금액: {format(self.bot.n_eth * amount,",")} ₩\n잔여 금액: {format(data[1],",")} ₩```',color=0xb40000)
                        elif amount == 0:
                            embed=discord.Embed(title="구매 수량이 올바르지 않습니다.",description='예)\n```ㅍ구매 비트코인 1```',color=0xb40000)
                        else:
                            coin = data[3] + amount
                            cur.execute("UPDATE user_data SET eth = %s WHERE id = %s",(coin, str(ctx.author.id)))
                            money = data[1] - (self.bot.n_eth * amount)
                            cur.execute("UPDATE user_data SET money = %s WHERE id = %s",(money, str(ctx.author.id)))
                            bought = data[9] + (self.bot.n_eth * amount)
                            cur.execute("UPDATE user_data SET b_eth = %s WHERE id = %s",(bought, str(ctx.author.id)))
                            embed=discord.Embed(title='구매 완료',description=f'```구매 수량: {amount}개\n보유 화폐: {coin}개\n구매 금액: {format(self.bot.n_eth * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)

                    elif _id == '라이트코인' or _id == 'ltc' or _id == '라이트':
                        if _all == True:
                            amount = data[1] // self.bot.n_ltc
                        if self.bot.n_ltc * amount > data[1]:
                            embed=discord.Embed(title='잔액이 부족합니다.',description=f'```구매 금액: {format(self.bot.n_ltc * amount,",")} ₩\n잔여 금액: {format(data[1],",")} ₩```',color=0xb40000)
                        elif amount == 0:
                            embed=discord.Embed(title="구매 수량이 올바르지 않습니다.",description='예)\n```ㅍ구매 비트코인 1```',color=0xb40000)
                        else:
                            coin = data[4] + amount
                            cur.execute("UPDATE user_data SET ltc = %s WHERE id = %s",(coin, str(ctx.author.id)))
                            money = data[1] - (self.bot.n_ltc * amount)
                            cur.execute("UPDATE user_data SET money = %s WHERE id = %s",(money, str(ctx.author.id)))
                            bought = data[10] + (self.bot.n_ltc * amount)
                            cur.execute("UPDATE user_data SET b_ltc = %s WHERE id = %s",(bought, str(ctx.author.id)))
                            embed=discord.Embed(title='구매 완료',description=f'```구매 수량: {amount}개\n보유 화폐: {coin}개\n구매 금액: {format(self.bot.n_ltc * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)

                    elif _id == '폴카닷' or _id == 'dot' or _id == '폴' or _id == '폴카':
                        if _all == True:
                            amount = data[1] // self.bot.n_dot
                        if self.bot.n_dot * amount > data[1]:
                            embed=discord.Embed(title='잔액이 부족합니다.',description=f'```구매 금액: {format(self.bot.n_dot * amount,",")} ₩\n잔여 금액: {format(data[1],",")} ₩```',color=0xb40000)
                        elif amount == 0:
                            embed=discord.Embed(title="구매 수량이 올바르지 않습니다.",description='예)\n```ㅍ구매 비트코인 1```',color=0xb40000)
                        else:
                            coin = data[5] + amount
                            cur.execute("UPDATE user_data SET dot = %s WHERE id = %s",(coin, str(ctx.author.id)))
                            money = data[1] - (self.bot.n_dot * amount)
                            cur.execute("UPDATE user_data SET money = %s WHERE id = %s",(money, str(ctx.author.id)))
                            bought = data[11] + (self.bot.n_dot * amount)
                            cur.execute("UPDATE user_data SET b_dot = %s WHERE id = %s",(bought, str(ctx.author.id)))
                            embed=discord.Embed(title='구매 완료',description=f'```구매 수량: {amount}개\n보유 화폐: {coin}개\n구매 금액: {format(self.bot.n_dot * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)

                    elif _id == '에이다' or _id == 'ada' or _id == '에' or _id == '에이':
                        if _all == True:
                            amount = data[1] // self.bot.n_ada
                        if self.bot.n_ada * amount > data[1]:
                            embed=discord.Embed(title='잔액이 부족합니다.',description=f'```구매 금액: {format(self.bot.n_ada * amount,",")} ₩\n잔여 금액: {format(data[1],",")} ₩```',color=0xb40000)
                        elif amount == 0:
                            embed=discord.Embed(title="구매 수량이 올바르지 않습니다.",description='예)\n```ㅍ구매 비트코인 1```',color=0xb40000)
                        else:
                            coin = data[6] + amount
                            cur.execute("UPDATE user_data SET ada = %s WHERE id = %s",(coin, str(ctx.author.id)))
                            money = data[1] - (self.bot.n_ada * amount)
                            cur.execute("UPDATE user_data SET money = %s WHERE id = %s",(money, str(ctx.author.id)))
                            bought = data[12] + (self.bot.n_ada * amount)
                            cur.execute("UPDATE user_data SET b_ada = %s WHERE id = %s",(bought, str(ctx.author.id)))
                            embed=discord.Embed(title='구매 완료',description=f'```구매 수량: {amount}개\n보유 화폐: {coin}개\n구매 금액: {format(self.bot.n_ada * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)

                    elif _id == '도지코인' or _id == 'doge' or _id == '도지':
                        if _all == True:
                            amount = data[1] // self.bot.n_doge
                        if self.bot.n_doge * amount > data[1]:
                            embed=discord.Embed(title='잔액이 부족합니다.',description=f'```구매 금액: {format(self.bot.n_doge * amount,",")} ₩\n잔여 금액: {format(data[1],",")} ₩```',color=0xb40000)
                        elif amount == 0:
                            embed=discord.Embed(title="구매 수량이 올바르지 않습니다.",description='예)\n```ㅍ구매 비트코인 1```',color=0xb40000)
                        else:
                            coin = data[7] + amount
                            cur.execute("UPDATE user_data SET doge = %s WHERE id = %s",(coin, str(ctx.author.id)))
                            money = data[1] - (self.bot.n_doge * amount)
                            cur.execute("UPDATE user_data SET money = %s WHERE id = %s",(money, str(ctx.author.id)))
                            bought = data[13] + (self.bot.n_doge * amount)
                            cur.execute("UPDATE user_data SET b_doge = %s WHERE id = %s",(bought, str(ctx.author.id)))
                            embed=discord.Embed(title='구매 완료',description=f'```구매 수량: {amount}개\n보유 화폐: {coin}개\n구매 금액: {format(self.bot.n_doge * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)

                    else:
                        embed=discord.Embed(title='이름을 정확히 적어주세요.',description='예)\n```ㅍ구매 비트코인 1```',color=0xb40000)
            conn.commit()
            conn.close()
        await ctx.send(embed=embed)

    @commands.command(aliases=["판매", "매도", "sell"])
    async def cmdSell(self, ctx, *args):
        try:
            _id = args[0]
            if args[1] == '모두' or args[1] == '전부' or args[1] == 'all':
                _all = True
                amount = 1
            else:
                _all = False
                amount = int(args[1])
        except:
            if len(args) != 2:
                embed=discord.Embed(title="인수의 개수가 올바르지 않습니다.",description='예)\n```ㅍ판매 비트코인 1```',color=0xb40000)
            else:
                embed=discord.Embed(title="판매 수량이 올바르지 않습니다.",description='예)\n```ㅍ판매 비트코인 1```',color=0xb40000)
        else:
            async with ctx.typing():
                DATABASE_URL = os.environ['DATABASE_URL']
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                cur = conn.cursor()
                cur.execute("SELECT * FROM user_data WHERE id = %s", (str(ctx.author.id),))
                data = cur.fetchone()
                if data == None:
                    cur.execute("INSERT INTO user_data VALUES (%s, 100000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)",(str(ctx.author.id),))
                    embed=discord.Embed(title="계좌가 없으시군요! 지금 만들어 드리겠습니다.", description='```계좌 생성 보너스: 100,000 ₩```', color=0x8be653)
                elif len(args) != 2:
                    embed=discord.Embed(title="인수의 개수가 올바르지 않습니다.",description='예)\n```ㅍ구매 비트코인 1```',color=0xb40000)
                elif amount < 1:
                    embed=discord.Embed(title="판매 수량이 올바르지 않습니다.",description='예)\n```ㅍ판매 비트코인 1```',color=0xb40000)
                else:
                    if _id == '비트코인' or _id == 'btc' or _id == '비트':
                        if _all == True:
                            amount = data[2]
                        if amount > data[2]:
                            embed=discord.Embed(title='보유 화폐가 부족합니다.',description=f'```판매 수량: {amount} 개\n보유 화폐: {data[2]} 개```',color=0xb40000)
                        elif amount == 0:
                            embed=discord.Embed(title="판매 수량이 올바르지 않습니다.",description='예)\n```ㅍ판매 비트코인 1```',color=0xb40000)
                        else:
                            coin = data[2] - amount
                            cur.execute("UPDATE user_data SET btc = %s WHERE id = %s",(coin, str(ctx.author.id)))
                            money = data[1] + (self.bot.n_btc * amount)
                            cur.execute("UPDATE user_data SET money = %s WHERE id = %s",(money, str(ctx.author.id)))
                            bought = data[8] - ((self.bot.n_btc * amount) - ((amount / data[2]) * (data[2] * self.bot.n_btc - data[8])))
                            cur.execute("UPDATE user_data SET b_btc = %s WHERE id = %s",(bought, str(ctx.author.id)))
                            embed=discord.Embed(title='판매 완료',description=f'```판매 수량: {amount}개\n보유 화폐: {coin}개\n판매 금액: {format(self.bot.n_btc * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)

                    elif _id == '이더리움' or _id == 'eth' or _id == '이더':
                        if _all == True:
                            amount = data[3]
                        if amount > data[3]:
                            embed=discord.Embed(title='보유 화폐가 부족합니다.',description=f'```판매 수량: {amount} 개\n보유 화폐: {data[3]} 개```',color=0xb40000)
                        elif amount == 0:
                            embed=discord.Embed(title="판매 수량이 올바르지 않습니다.",description='예)\n```ㅍ판매 비트코인 1```',color=0xb40000)
                        else:
                            coin = data[3] - amount
                            cur.execute("UPDATE user_data SET eth = %s WHERE id = %s",(coin, str(ctx.author.id)))
                            money = data[1] + (self.bot.n_eth * amount)
                            cur.execute("UPDATE user_data SET money = %s WHERE id = %s",(money, str(ctx.author.id)))
                            bought = data[9] - ((self.bot.n_eth * amount) - ((amount / data[3]) * (data[3] * self.bot.n_eth - data[9])))
                            cur.execute("UPDATE user_data SET b_eth = %s WHERE id = %s",(bought, str(ctx.author.id)))
                            embed=discord.Embed(title='판매 완료',description=f'```판매 수량: {amount}개\n보유 화폐: {coin}개\n판매 금액: {format(self.bot.n_eth * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)

                    elif _id == '라이트코인' or _id == 'ltc' or _id == '라이트':
                        if _all == True:
                            amount = data[4]
                        if amount > data[4]:
                            embed=discord.Embed(title='보유 화폐가 부족합니다.',description=f'```판매 수량: {amount} 개\n보유 화폐: {data[4]} 개```',color=0xb40000)
                        elif amount == 0:
                            embed=discord.Embed(title="판매 수량이 올바르지 않습니다.",description='예)\n```ㅍ판매 비트코인 1```',color=0xb40000)
                        else:
                            coin = data[4] - amount
                            cur.execute("UPDATE user_data SET ltc = %s WHERE id = %s",(coin, str(ctx.author.id)))
                            money = data[1] + (self.bot.n_ltc * amount)
                            cur.execute("UPDATE user_data SET money = %s WHERE id = %s",(money, str(ctx.author.id)))
                            bought = data[10] - ((self.bot.n_ltc * amount) - ((amount / data[4]) * (data[4] * self.bot.n_ltc - data[10])))
                            cur.execute("UPDATE user_data SET b_ltc = %s WHERE id = %s",(bought, str(ctx.author.id)))
                            embed=discord.Embed(title='판매 완료',description=f'```판매 수량: {amount}개\n보유 화폐: {coin}개\n판매 금액: {format(self.bot.n_ltc * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)

                    elif _id == '폴카닷' or _id == 'dot' or _id == '폴' or _id == '폴카':
                        if _all == True:
                            amount = data[5]
                        if amount > data[5]:
                            embed=discord.Embed(title='보유 화폐가 부족합니다.',description=f'```판매 수량: {amount} 개\n보유 화폐: {data[5]} 개```',color=0xb40000)
                        elif amount == 0:
                            embed=discord.Embed(title="판매 수량이 올바르지 않습니다.",description='예)\n```ㅍ판매 비트코인 1```',color=0xb40000)
                        else:
                            coin = data[5] - amount
                            cur.execute("UPDATE user_data SET dot = %s WHERE id = %s",(coin, str(ctx.author.id)))
                            money = data[1] + (self.bot.n_dot * amount)
                            cur.execute("UPDATE user_data SET money = %s WHERE id = %s",(money, str(ctx.author.id)))
                            bought = data[11] - ((self.bot.n_dot * amount) - ((amount / data[5]) * (data[5] * self.bot.n_dot - data[11])))
                            cur.execute("UPDATE user_data SET b_dot = %s WHERE id = %s",(bought, str(ctx.author.id)))
                            embed=discord.Embed(title='판매 완료',description=f'```판매 수량: {amount}개\n보유 화폐: {coin}개\n판매 금액: {format(self.bot.n_dot * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)

                    elif _id == '에이다' or _id == 'ada' or _id == '에' or _id == '에이':
                        if _all == True:
                            amount = data[6]
                        if amount > data[6]:
                            embed=discord.Embed(title='보유 화폐가 부족합니다.',description=f'```판매 수량: {amount} 개\n보유 화폐: {data[6]} 개```',color=0xb40000)
                        elif amount == 0:
                            embed=discord.Embed(title="판매 수량이 올바르지 않습니다.",description='예)\n```ㅍ판매 비트코인 1```',color=0xb40000)
                        else:
                            coin = data[6] - amount
                            cur.execute("UPDATE user_data SET ada = %s WHERE id = %s",(coin, str(ctx.author.id)))
                            money = data[1] + (self.bot.n_ada * amount)
                            cur.execute("UPDATE user_data SET money = %s WHERE id = %s",(money, str(ctx.author.id)))
                            bought = data[12] - ((self.bot.n_ada * amount) - ((amount / data[6]) * (data[6] * self.bot.n_ada - data[12])))
                            cur.execute("UPDATE user_data SET b_ada = %s WHERE id = %s",(bought, str(ctx.author.id)))
                            embed=discord.Embed(title='판매 완료',description=f'```판매 수량: {amount}개\n보유 화폐: {coin}개\n판매 금액: {format(self.bot.n_ada * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)

                    elif _id == '도지코인' or _id == 'doge' or _id == '도지':
                        if _all == True:
                            amount = data[7]
                        if amount > data[7]:
                            embed=discord.Embed(title='보유 화폐가 부족합니다.',description=f'```판매 수량: {amount} 개\n보유 화폐: {data[7]} 개```',color=0xb40000)
                        elif amount == 0:
                            embed=discord.Embed(title="판매 수량이 올바르지 않습니다.",description='예)\n```ㅍ판매 비트코인 1```',color=0xb40000)
                        else:
                            coin = data[7] - amount
                            cur.execute("UPDATE user_data SET doge = %s WHERE id = %s",(coin, str(ctx.author.id)))
                            money = data[1] + (self.bot.n_doge * amount)
                            cur.execute("UPDATE user_data SET money = %s WHERE id = %s",(money, str(ctx.author.id)))
                            bought = data[13] - ((self.bot.n_doge * amount) - ((amount / data[7]) * (data[7] * self.bot.n_doge - data[13])))
                            cur.execute("UPDATE user_data SET b_doge = %s WHERE id = %s",(bought, str(ctx.author.id)))
                            embed=discord.Embed(title='판매 완료',description=f'```판매 수량: {amount}개\n보유 화폐: {coin}개\n판매 금액: {format(self.bot.n_doge * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)

                    else:
                        embed=discord.Embed(title='이름을 정확히 적어주세요.',description='예)\n```ㅍ판매 비트코인 1```',color=0xb40000)
                conn.commit()
                conn.close()
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["지갑", "계좌", "정보", "돈", "wallet", "info", "money"])
    async def cmdInfo(self, ctx):
        async with ctx.typing():
            DATABASE_URL = os.environ['DATABASE_URL']
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            cur.execute("SELECT * FROM user_data WHERE id = %s", (str(ctx.author.id),))
            data = cur.fetchone()
            if data == None:
                cur.execute("INSERT INTO user_data VALUES (%s, 100000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)",(str(ctx.author.id),))
                embed=discord.Embed(title="계좌가 없으시군요! 지금 만들어 드리겠습니다.", description='```계좌 생성 보너스: 100,000 ₩```', color=0x8be653)
            else:
                all_money = data[1] + (self.bot.n_btc * data[2]) + (self.bot.n_eth * data[3]) + (self.bot.n_ltc * data[4]) + (self.bot.n_dot * data[5]) + (self.bot.n_ada * data[6]) + (self.bot.n_doge * data[7])
                e_btc = format(int(self.bot.n_btc * data[2] - data[8]),',')
                e_eth = format(int(self.bot.n_eth * data[3] - data[9]),',')
                e_ltc = format(int(self.bot.n_ltc * data[4] - data[10]),',')
                e_dot = format(int(self.bot.n_dot * data[5] - data[11]),',')
                e_ada = format(int(self.bot.n_ada * data[6] - data[12]),',')
                e_doge = format(int(self.bot.n_doge * data[7] - data[13]),',')
                embed=discord.Embed(title="계좌 정보", description=f"```bash\n총자산: {format(all_money,',')} ₩\n잔액　: {format(data[1],',')} ₩\n\n비트코인　: {data[2]} # 손익 : {e_btc} ₩\n이더리움　: {data[3]} # 손익 : {e_eth} ₩\n라이트코인: {data[4]} # 손익 : {e_ltc} ₩\n폴카닷　　: {data[5]} # 손익 : {e_dot} ₩\n에이다　　: {data[6]} # 손익 : {e_ada} ₩\n도지코인　: {data[7]} # 손익 : {e_doge} ₩```", color=0x8be653)
            conn.commit()
            conn.close()
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["용돈", "daily", "돈받기", "월급", "일일보상", "일일"])
    async def cmdDaily(self, ctx):
        async with ctx.typing():
            DATABASE_URL = os.environ['DATABASE_URL']
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            cur.execute("SELECT * FROM user_data WHERE id = %s", (str(ctx.author.id),))
            data = cur.fetchone()
            if data == None:
                cur.execute("INSERT INTO user_data VALUES (%s, 100000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)",(str(ctx.author.id),))
                embed=discord.Embed(title="계좌가 없으시군요! 지금 만들어 드리겠습니다.", description='```계좌 생성 보너스: 100,000 ₩```', color=0x8be653)
            else:
                if data[14] == 1:
                    money = data[1] + 10000
                    cur.execute("UPDATE user_data SET money = %s WHERE id = %s",(money, str(ctx.author.id)))
                    cur.execute("UPDATE user_data SET daily = %s WHERE id = %s",(0, str(ctx.author.id)))
                    embed=discord.Embed(title="일일 보상을 받았습니다!", description=f'```일일 보상: 10,000 ₩\n잔여 금액: {format(money,",")} ₩```', color=0x8be653)
                else:
                    time = ''
                    if self.bot.h != '':
                        time += f'{self.bot.h}시간 '
                    if self.bot.m != '':
                        time += f'{self.bot.m}분 '
                    time += f'{self.bot.s}초'
                    embed=discord.Embed(title='이미 일일 보상을 받았습니다.',description=f'```남은 시간: {time}```',color=0xb40000)
                    embed.set_footer(text=f'`UTC 00:00`에 초기화')
            conn.commit()
            conn.close()
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["한강", "한강온도", "한강물"])
    async def cmdHangang(self, ctx):
        async with ctx.typing():
            url = 'https://api.qwer.pw/request/hangang_temp'
            params = {'apikey': 'guest'}
            res = requests.get(url, params=params)
            try:
                temp = res.json()[1]['respond']['temp']
            except:
                embed=discord.Embed(title='오류가 발생했습니다.',color=0xb40000)
            else:
                embed=discord.Embed(title='현재 한강물 온도', description=f'```{temp}℃```', color=0x3a94ce)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["그래프", "graph", "표", "그"])
    async def cmdGraph(self, ctx):
        async with ctx.typing():
            image = discord.File('graph.png')
        await ctx.send(file=image)
    
    @commands.command(aliases=["랭킹", "순위", "랭크", "ranking", "rank"])
    async def cmdRank(self, ctx):
        async with ctx.typing():
            DATABASE_URL = os.environ['DATABASE_URL']
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            cur.execute("SELECT * FROM user_data")
            data = cur.fetchall()
            des = '```'
            m_data = []
            for i in range(0,len(data)):
                user = await self.bot.fetch_user(data[i][0])
                all_money = data[i][1] + (self.bot.n_btc * data[i][2]) + (self.bot.n_eth * data[i][3]) + (self.bot.n_ltc * data[i][4]) + (self.bot.n_dot * data[i][5]) + (self.bot.n_ada * data[i][6]) + (self.bot.n_doge * data[i][7])
                m_data.append((str(user), all_money))
            m_data.sort(key=lambda x:x[1], reverse=True)
            for j in range(0,len(m_data)):
                des += f'{j+1}. {m_data[j][0]} | {format(m_data[j][1],",")} ₩\n'
            des += '```'
            embed=discord.Embed(title='자산 순위 TOP 10',description=des,color=0x8be653)
            conn.close()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(cmdCoin(bot))