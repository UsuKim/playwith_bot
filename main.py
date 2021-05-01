import asyncio,discord,os,random,psycopg2,datetime,matplotlib
from upbitpy import Upbitpy
from discord.ext import commands, tasks
from itertools import cycle
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.font_manager

# https://discord.com/oauth2/authorize?client_id=835763308509396993&scope=bot

# 업비트
upbit = Upbitpy()

# 토큰 가져오기
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

# 초당 실행
@tasks.loop(seconds=1)
async def change_time():
    bot.time -= 1
    today = datetime.datetime.today()
    tomorrow = today + timedelta(days=1)
    t = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0) - today
    bot.h = t.seconds // 3600
    bot.m = (t.seconds % 3600) // 60
    bot.s = t.seconds % 60
    if bot.h == 0:
        bot.h = ''
    if bot.m == 0:
        bot.m = ''
    if t.seconds == 0:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("SELECT * FROM user_data")
        cur.execute("UPDATE user_data SET daily = %s",(1,))
        conn.commit()
        conn.close()

# 가격 불러오기
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
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT * FROM graph_data")
    data = cur.fetchall()
    if len(data) < 100:
        cur.execute("INSERT INTO graph_data VALUES (%s, %s, %s, %s, %s, %s, %s)",(data[-1][0]+1, bot.n_btc, bot.n_eth, bot.n_ltc, bot.n_dot, bot.n_ada, bot.n_doge))
    else:
        cur.execute("DELETE FROM graph_data WHERE id = %s",(data[0][0],))
        cur.execute("INSERT INTO graph_data VALUES (%s, %s, %s, %s, %s, %s, %s)",(data[-1][0]+1, bot.n_btc, bot.n_eth, bot.n_ltc, bot.n_dot, bot.n_ada, bot.n_doge))
    conn.commit()
    cur.execute("SELECT * FROM graph_data")
    data = cur.fetchall()
    conn.close()
    btc = []
    eth = []
    ltc = []
    dot = []
    ada = []
    doge = []
    time = []
    for i in range(len(data)):
        btc.append(data[i][1])
        eth.append(data[i][2])
        ltc.append(data[i][3])
        dot.append(data[i][4])
        ada.append(data[i][5])
        doge.append(data[i][6])
        time.append(i*3/60)
    matplotlib.rcParams['axes.unicode_minus'] = False
    matplotlib.rcParams['font.family'] = "NanumGothicCoding"
    plt.figure()
    plt.plot(time, btc, color='darkorange', label="비트코인")
    plt.ylim([min(btc)-min(btc)/500, max(btc)+max(btc)/500])
    plt.xlabel('시간 (h)')
    plt.tick_params(axis='y', length=0, labelcolor='white')
    plt.legend(loc=(0.01, 0.92), framealpha=0.8)
    plt.twinx()
    plt.plot(time, eth, color='skyblue', label="이더리움")
    plt.ylim([min(eth)-min(eth)/500, max(eth)+max(eth)/500])
    plt.tick_params(axis='y', length=0, labelcolor='white')
    plt.legend(loc=(0.01, 0.85), framealpha=0.8)
    plt.twinx()
    plt.plot(time, ltc, color='royalblue', label="라이트코인")
    plt.ylim([min(ltc)-min(ltc)/500, max(ltc)+max(ltc)/500])
    plt.tick_params(axis='y', length=0, labelcolor='white')
    plt.legend(loc=(0.01, 0.78), framealpha=0.8)
    plt.twinx()
    plt.plot(time, dot, color='mediumvioletred', label="폴카닷")
    plt.ylim([min(dot)-min(dot)/500, max(dot)+max(dot)/500])
    plt.tick_params(axis='y', length=0, labelcolor='white')
    plt.legend(loc=(0.01, 0.71), framealpha=0.8)
    plt.twinx()
    plt.plot(time, ada, color='midnightblue', label="에이다")
    plt.ylim([min(ada)-min(ada)/500, max(ada)+max(ada)/500])
    plt.tick_params(axis='y', length=0, labelcolor='white')
    plt.legend(loc=(0.01, 0.64), framealpha=0.8)
    plt.twinx()
    plt.plot(time, doge, color='gold', label="도지코인")
    plt.ylim([min(doge)-min(doge)/500, max(doge)+max(doge)/500])
    plt.tick_params(axis='y', length=0, labelcolor='white')
    plt.legend(loc=(0.01, 0.57), framealpha=0.8)
    plt.title('주식 그래프', loc='right')
    plt.savefig('graph.png')
    print(btc, eth, ltc, dot, ada, doge, time)

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