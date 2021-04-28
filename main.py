import asyncio,discord,os,random,sqlite3
from upbitpy import Upbitpy
from discord.ext import commands, tasks
from itertools import cycle

# 업비트
upbit = Upbitpy()

#토큰 가져오기
token_path = os.path.dirname( os.path.abspath( __file__ ) )+"/token.txt"
t = open(token_path,"r",encoding="utf-8")
token = t.read().split()[0]

# 봇 설정
game = discord.Game("ㅍ도움")
bot = commands.Bot(command_prefix='ㅍ',status=discord.Status.online,activity=game)
bot.remove_command("help") #help 명령어 지우기
playing = cycle(["ㅍ도움", "ㅍ도움말", "ㅍhelp"])
bot.time = 0
bot.btc, bot.eth, bot.doge, bot.ada, bot.dot, bot.ltc = 0,0,0,0,0,0
markets = upbit.get_market_all()
krw_markets = []
for market in markets:
    if 'KRW-' in market['market']:
        krw_markets.append(market['market'])
ticker = upbit.get_ticker(krw_markets)
for it in ticker:
    if it['market'] == 'KRW-BTC':
        bot.n_btc = int(it['trade_price'])
    if it['market'] == 'KRW-ETH':
        bot.n_eth = int(it['trade_price'])
    if it['market'] == 'KRW-DOGE':
        bot.n_doge = int(it['trade_price'])
    if it['market'] == 'KRW-ADA':
        bot.n_ada = int(it['trade_price'])
    if it['market'] == 'KRW-DOT':
        bot.n_dot = int(it['trade_price'])
    if it['market'] == 'KRW-LTC':
        bot.n_ltc = int(it['trade_price'])

# cog 설정
for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

# 상메 바꾸기
@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(playing)))

@tasks.loop(seconds=1)
async def change_time():
    bot.time -= 1

#가격 불러오기
@tasks.loop(seconds=180)
async def change_price():
    bot.btc, bot.eth, bot.doge, bot.ada, bot.dot, bot.ltc = bot.n_btc, bot.n_eth, bot.n_doge, bot.n_ada, bot.n_dot, bot.n_ltc
    markets = upbit.get_market_all()
    krw_markets = []
    for market in markets:
        if 'KRW-' in market['market']:
            krw_markets.append(market['market'])
    ticker = upbit.get_ticker(krw_markets)
    for it in ticker:
        if it['market'] == 'KRW-BTC':
            bot.n_btc = int(it['trade_price'])
        if it['market'] == 'KRW-ETH':
            bot.n_eth = int(it['trade_price'])
        if it['market'] == 'KRW-DOGE':
            bot.n_doge = int(it['trade_price'])
        if it['market'] == 'KRW-ADA':
            bot.n_ada = int(it['trade_price'])
        if it['market'] == 'KRW-DOT':
            bot.n_dot = int(it['trade_price'])
        if it['market'] == 'KRW-LTC':
            bot.n_ltc = int(it['trade_price'])
    bot.r_btc = bot.n_btc - bot.btc
    bot.r_eth = bot.n_eth - bot.eth
    bot.r_doge = bot.n_doge - bot.doge
    bot.r_ada = bot.n_ada - bot.ada
    bot.r_dot = bot.n_dot - bot.dot
    bot.r_ltc = bot.n_ltc - bot.ltc
    bot.time = 180
    print('가격 갱신 완료')

# 봇 시작
@bot.event
async def on_ready():
    print("/// 다음으로 로그인 됨: ///")
    print(bot.user.name)
    print(bot.user.id)
    print("===========================")
    change_status.start()
    change_price.start()
    change_time.start()

# 리로드 커맨드
@bot.command(aliases=["리로드", "리", "reload", "re"])
async def reload_commands(ctx, extension=None):
    if ctx.message.author.id == 378095367599685633:
        if extension is None: # extension이 None이면 (그냥 //리로드 라고 썼을 때)
            for filename in os.listdir("cogs"):
                if filename.endswith(".py"):
                    bot.unload_extension(f"cogs.{filename[:-3]}")
                    bot.load_extension(f"cogs.{filename[:-3]}")
            await ctx.message.add_reaction('✅')
        else:
            bot.unload_extension(f"cogs.{extension}")
            bot.load_extension(f"cogs.{extension}")
            await ctx.send(f":white_check_mark: {extension}을(를) 다시 불러왔습니다!")
    else:
        await ctx.message.add_reaction('⛔')

bot.run(token)