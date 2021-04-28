import asyncio,discord,os,random,sqlite3
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
    async def cmdBuy(self, ctx, id: str, amount: int):
        async with ctx.typing():
            conn = sqlite3.connect("price.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM user_data WHERE id = ?",(ctx.author.id,))
            data = cur.fetchone()
            if data == None:
                cur.execute("INSERT INTO user_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(ctx.author.id, 100000, 0, 0, 0, 0, 0, 0, 1))
                embed=discord.Embed(title="계좌가 없으시군요! 지금 만들어 드리겠습니다.", description='```계좌 생성 보너스: 100,000 ₩```', color=0x8be653)
            elif amount < 1:
                embed=discord.Embed(title="구매 수량이 올바르지 않습니다.",description='예)\n```ㅍ구매 비트코인 1```',color=0xb40000)
            else:
                if id == '비트코인' or id == 'btc' or id == '비트':
                    if self.bot.n_btc * amount > data[1]:
                        embed=discord.Embed(title='잔액이 부족합니다.',description=f'```구매 금액: {format(self.bot.n_btc * amount,",")} ₩\n잔여 금액: {format(data[1],",")} ₩```',color=0xb40000)
                    else:
                        coin = data[2] + amount
                        cur.execute("UPDATE user_data SET btc = ? WHERE id = ?",(coin, ctx.author.id))
                        money = data[1] - (self.bot.n_btc * amount)
                        cur.execute("UPDATE user_data SET money = ? WHERE id = ?",(money, ctx.author.id))
                        embed=discord.Embed(title='구매 완료',description=f'```구매 수량: {amount}개\n보유 화폐: {coin}개\n구매 금액: {format(self.bot.n_btc * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)
                
                elif id == '이더리움' or id == 'eth' or id == '이더':
                    if self.bot.n_eth * amount > data[1]:
                        embed=discord.Embed(title='잔액이 부족합니다.',description=f'```구매 금액: {format(self.bot.n_eth * amount,",")} ₩\n잔여 금액: {format(data[1],",")} ₩```',color=0xb40000)
                    else:
                        coin = data[3] + amount
                        cur.execute("UPDATE user_data SET eth = ? WHERE id = ?",(coin, ctx.author.id))
                        money = data[1] - (self.bot.n_eth * amount)
                        cur.execute("UPDATE user_data SET money = ? WHERE id = ?",(money, ctx.author.id))
                        embed=discord.Embed(title='구매 완료',description=f'```구매 수량: {amount}개\n보유 화폐: {coin}개\n구매 금액: {format(self.bot.n_eth * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)
                
                elif id == '라이트코인' or id == 'ltc' or id == '라이트':
                    if self.bot.n_ltc * amount > data[1]:
                        embed=discord.Embed(title='잔액이 부족합니다.',description=f'```구매 금액: {format(self.bot.n_ltc * amount,",")} ₩\n잔여 금액: {format(data[1],",")} ₩```',color=0xb40000)
                    else:
                        coin = data[4] + amount
                        cur.execute("UPDATE user_data SET ltc = ? WHERE id = ?",(coin, ctx.author.id))
                        money = data[1] - (self.bot.n_ltc * amount)
                        cur.execute("UPDATE user_data SET money = ? WHERE id = ?",(money, ctx.author.id))
                        embed=discord.Embed(title='구매 완료',description=f'```구매 수량: {amount}개\n보유 화폐: {coin}개\n구매 금액: {format(self.bot.n_ltc * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)
                
                elif id == '폴카닷' or id == 'dot' or id == '폴' or id == '폴카':
                    if self.bot.n_dot * amount > data[1]:
                        embed=discord.Embed(title='잔액이 부족합니다.',description=f'```구매 금액: {format(self.bot.n_dot * amount,",")} ₩\n잔여 금액: {format(data[1],",")} ₩```',color=0xb40000)
                    else:
                        coin = data[5] + amount
                        cur.execute("UPDATE user_data SET dot = ? WHERE id = ?",(coin, ctx.author.id))
                        money = data[1] - (self.bot.n_dot * amount)
                        cur.execute("UPDATE user_data SET money = ? WHERE id = ?",(money, ctx.author.id))
                        embed=discord.Embed(title='구매 완료',description=f'```구매 수량: {amount}개\n보유 화폐: {coin}개\n구매 금액: {format(self.bot.n_dot * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)
                
                elif id == '에이다' or id == 'ada' or id == '에' or id == '에이':
                    if self.bot.n_ada * amount > data[1]:
                        embed=discord.Embed(title='잔액이 부족합니다.',description=f'```구매 금액: {format(self.bot.n_ada * amount,",")} ₩\n잔여 금액: {format(data[1],",")} ₩```',color=0xb40000)
                    else:
                        coin = data[6] + amount
                        cur.execute("UPDATE user_data SET ada = ? WHERE id = ?",(coin, ctx.author.id))
                        money = data[1] - (self.bot.n_ada * amount)
                        cur.execute("UPDATE user_data SET money = ? WHERE id = ?",(money, ctx.author.id))
                        embed=discord.Embed(title='구매 완료',description=f'```구매 수량: {amount}개\n보유 화폐: {coin}개\n구매 금액: {format(self.bot.n_ada * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)
                
                elif id == '도지코인' or id == 'doge' or id == '도지':
                    if self.bot.n_doge * amount > data[1]:
                        embed=discord.Embed(title='잔액이 부족합니다.',description=f'```구매 금액: {format(self.bot.n_doge * amount,",")} ₩\n잔여 금액: {format(data[1],",")} ₩```',color=0xb40000)
                    else:
                        coin = data[7] + amount
                        cur.execute("UPDATE user_data SET doge = ? WHERE id = ?",(coin, ctx.author.id))
                        money = data[1] - (self.bot.n_doge * amount)
                        cur.execute("UPDATE user_data SET money = ? WHERE id = ?",(money, ctx.author.id))
                        embed=discord.Embed(title='구매 완료',description=f'```구매 수량: {amount}개\n보유 화폐: {coin}개\n구매 금액: {format(self.bot.n_doge * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)

                else:
                    embed=discord.Embed(title='이름을 정확히 적어주세요.',description='예)\n```ㅍ구매 비트코인 1```',color=0xb40000)
            conn.commit()
            conn.close()
        await ctx.send(embed=embed)

    @commands.command(aliases=["판매", "매도", "sell"])
    async def cmdSell(self, ctx, id: str, amount: int):
        async with ctx.typing():
            conn = sqlite3.connect("price.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM user_data WHERE id = ?",(ctx.author.id,))
            data = cur.fetchone()
            if data == None:
                cur.execute("INSERT INTO user_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(ctx.author.id, 100000, 0, 0, 0, 0, 0, 0, 1))
                embed=discord.Embed(title="계좌가 없으시군요! 지금 만들어 드리겠습니다.", description='```계좌 생성 보너스: 100,000 ₩```', color=0x8be653)
            elif amount < 1:
                embed=discord.Embed(title="판매 수량이 올바르지 않습니다.",description='예)\n```ㅍ판매 비트코인 1```',color=0xb40000)
            else:
                if id == '비트코인' or id == 'btc' or id == '비트':
                    if amount > data[2]:
                        embed=discord.Embed(title='보유 화폐가 부족합니다.',description=f'```판매 수량: {amount} 개\n보유 화폐: {data[2]} 개```',color=0xb40000)
                    else:
                        coin = data[2] - amount
                        cur.execute("UPDATE user_data SET btc = ? WHERE id = ?",(coin, ctx.author.id))
                        money = data[1] + (self.bot.n_btc * amount)
                        cur.execute("UPDATE user_data SET money = ? WHERE id = ?",(money, ctx.author.id))
                        embed=discord.Embed(title='판매 완료',description=f'```판매 수량: {amount}개\n보유 화폐: {coin}개\n판매 금액: {format(self.bot.n_btc * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)
                
                elif id == '이더리움' or id == 'eth' or id == '이더':
                    if amount > data[3]:
                        embed=discord.Embed(title='보유 화폐가 부족합니다.',description=f'```판매 수량: {amount} 개\n보유 화폐: {data[2]} 개```',color=0xb40000)
                    else:
                        coin = data[3] - amount
                        cur.execute("UPDATE user_data SET eth = ? WHERE id = ?",(coin, ctx.author.id))
                        money = data[1] + (self.bot.n_eth * amount)
                        cur.execute("UPDATE user_data SET money = ? WHERE id = ?",(money, ctx.author.id))
                        embed=discord.Embed(title='판매 완료',description=f'```판매 수량: {amount}개\n보유 화폐: {coin}개\n판매 금액: {format(self.bot.n_eth * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)
                
                elif id == '라이트코인' or id == 'ltc' or id == '라이트':
                    if amount > data[4]:
                        embed=discord.Embed(title='보유 화폐가 부족합니다.',description=f'```판매 수량: {amount} 개\n보유 화폐: {data[2]} 개```',color=0xb40000)
                    else:
                        coin = data[4] - amount
                        cur.execute("UPDATE user_data SET ltc = ? WHERE id = ?",(coin, ctx.author.id))
                        money = data[1] + (self.bot.n_ltc * amount)
                        cur.execute("UPDATE user_data SET money = ? WHERE id = ?",(money, ctx.author.id))
                        embed=discord.Embed(title='판매 완료',description=f'```판매 수량: {amount}개\n보유 화폐: {coin}개\n판매 금액: {format(self.bot.n_ltc * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)
                
                elif id == '폴카닷' or id == 'dot' or id == '폴' or id == '폴카':
                    if amount > data[5]:
                        embed=discord.Embed(title='보유 화폐가 부족합니다.',description=f'```판매 수량: {amount} 개\n보유 화폐: {data[2]} 개```',color=0xb40000)
                    else:
                        coin = data[5] - amount
                        cur.execute("UPDATE user_data SET dot = ? WHERE id = ?",(coin, ctx.author.id))
                        money = data[1] + (self.bot.n_dot * amount)
                        cur.execute("UPDATE user_data SET money = ? WHERE id = ?",(money, ctx.author.id))
                        embed=discord.Embed(title='판매 완료',description=f'```판매 수량: {amount}개\n보유 화폐: {coin}개\n판매 금액: {format(self.bot.n_dot * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)
                
                elif id == '에이다' or id == 'ada' or id == '에' or id == '에이':
                    if amount > data[6]:
                        embed=discord.Embed(title='보유 화폐가 부족합니다.',description=f'```판매 수량: {amount} 개\n보유 화폐: {data[2]} 개```',color=0xb40000)
                    else:
                        coin = data[6] - amount
                        cur.execute("UPDATE user_data SET ada = ? WHERE id = ?",(coin, ctx.author.id))
                        money = data[1] + (self.bot.n_ada * amount)
                        cur.execute("UPDATE user_data SET money = ? WHERE id = ?",(money, ctx.author.id))
                        embed=discord.Embed(title='판매 완료',description=f'```판매 수량: {amount}개\n보유 화폐: {coin}개\n판매 금액: {format(self.bot.n_ada * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)
                
                elif id == '도지코인' or id == 'doge' or id == '도지':
                    if amount > data[7]:
                        embed=discord.Embed(title='보유 화폐가 부족합니다.',description=f'```판매 수량: {amount} 개\n보유 화폐: {data[2]} 개```',color=0xb40000)
                    else:
                        coin = data[7] - amount
                        cur.execute("UPDATE user_data SET doge = ? WHERE id = ?",(coin, ctx.author.id))
                        money = data[1] + (self.bot.n_doge * amount)
                        cur.execute("UPDATE user_data SET money = ? WHERE id = ?",(money, ctx.author.id))
                        embed=discord.Embed(title='판매 완료',description=f'```판매 수량: {amount}개\n보유 화폐: {coin}개\n판매 금액: {format(self.bot.n_doge * amount,",")} ₩\n잔여 금액: {format(money,",")} ₩```',color=0x8be653)
                
                else:
                    embed=discord.Embed(title='이름을 정확히 적어주세요.',description='예)\n```ㅍ판매 비트코인 1```',color=0xb40000)
            conn.commit()
            conn.close()
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["지갑", "계좌", "정보", "wallet", "info"])
    async def cmdInfo(self, ctx):
        async with ctx.typing():
            conn = sqlite3.connect("price.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM user_data WHERE id = ?",(ctx.author.id,))
            data = cur.fetchone()
            if data == None:
                cur.execute("INSERT INTO user_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(ctx.author.id, 100000, 0, 0, 0, 0, 0, 0, 1))
                embed=discord.Embed(title="계좌가 없으시군요! 지금 만들어 드리겠습니다.", description='```계좌 생성 보너스: 100,000 ₩```', color=0x8be653)
            else:
                all_money = data[1] + (self.bot.n_btc * data[2]) + (self.bot.n_eth * data[3]) + (self.bot.n_ltc * data[4]) + (self.bot.n_dot * data[5]) + (self.bot.n_ada * data[6]) + (self.bot.n_doge * data[7])
                embed=discord.Embed(title="계좌 정보", description=f"```총자산: {format(all_money,',')} ₩\n잔액　: {format(data[1],',')} ₩\n\n비트코인　: {data[2]}\n이더리움　: {data[3]}\n라이트코인: {data[4]}\n폴카닷　　: {data[5]}\n에이다　　: {data[6]}\n도지코인　: {data[7]}```", color=0x8be653)
            conn.commit()
            conn.close()
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(cmdCoin(bot))