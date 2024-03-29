import asyncio,discord,os,random,psycopg2,datetime,matplotlib
from upbitpy import Upbitpy
from discord.ext import commands, tasks
from itertools import cycle
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.font_manager

# https://discord.com/api/oauth2/authorize?client_id=835763308509396993&permissions=8&scope=bot%20applications.commands

# 업비트
upbit = Upbitpy()

# 토큰 가져오기
token = os.environ['TOKEN']

# 봇 설정
game = discord.Game("ㅍ도움")
bot = commands.Bot(command_prefix='ㅍ',status=discord.Status.online,activity=game)
bot.remove_command("help") #help 명령어 지우기
playing = cycle(["ㅍ도움", "ㅍ도움말", "ㅍhelp"])
bot.time = 0
bot.btc, bot.eth, bot.doge, bot.ada, bot.dot, bot.ltc, bot.xrp, bot.trx = 0,0,0,0,0,0,0,0
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
    if it['market'] == 'KRW-XRP':
            bot.n_xrp = int(it['trade_price'])
    if it['market'] == 'KRW-TRX':
        bot.n_trx = int(it['trade_price'])

# 데이터베이스 연결
DATABASE_URL = os.environ['DATABASE_URL']
bot.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
bot.cur = bot.conn.cursor()
bot.cur.execute("UPDATE user_data SET wait = 0")

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
        bot.cur.execute("SELECT * FROM user_data")
        bot.cur.execute("UPDATE user_data SET daily = %s",(1,))
        bot.conn.commit()

# btc eth ltc dot ada doge xrp trx

# 가격 불러오기
@tasks.loop(seconds=180)
async def change_price():
    bot.btc, bot.eth, bot.doge, bot.ada, bot.dot, bot.ltc, bot.xrp, bot.trx = bot.n_btc, bot.n_eth, bot.n_doge, bot.n_ada, bot.n_dot, bot.n_ltc, bot.n_xrp, bot.n_trx
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
        if it['market'] == 'KRW-XRP':
            bot.n_xrp = int(it['trade_price'])
        if it['market'] == 'KRW-TRX':
            bot.n_trx = int(it['trade_price'])
    bot.r_btc = bot.n_btc - bot.btc
    bot.r_eth = bot.n_eth - bot.eth
    bot.r_doge = bot.n_doge - bot.doge
    bot.r_ada = bot.n_ada - bot.ada
    bot.r_dot = bot.n_dot - bot.dot
    bot.r_ltc = bot.n_ltc - bot.ltc
    bot.r_xrp = bot.n_xrp - bot.xrp
    bot.r_trx = bot.n_trx - bot.trx
    bot.time = 180
    bot.cur.execute("SELECT * FROM graph_data")
    data = bot.cur.fetchall()
    today = datetime.datetime.today()
    time = f'{today.year}-{today.month}-{today.day} {today.hour}:{today.minute}:{today.second}'
    bot.cur.execute("INSERT INTO graph_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(time, bot.n_btc, bot.n_eth, bot.n_ltc, bot.n_dot, bot.n_ada, bot.n_doge, bot.n_xrp, bot.n_trx))
    if len(data) > 200:
        bot.cur.execute("DELETE FROM graph_data WHERE date IN (SELECT date FROM graph_data ORDER BY date asc LIMIT 1)")

    bot.conn.commit()
    bot.cur.execute("SELECT * FROM graph_data ORDER BY date asc")
    data = bot.cur.fetchall()
    btc = []
    eth = []
    ltc = []
    dot = []
    ada = []
    doge = []
    xrp = []
    trx = []
    time = []
    for i in range(len(data)):
        btc.append(data[i][1])
        eth.append(data[i][2])
        ltc.append(data[i][3])
        dot.append(data[i][4])
        ada.append(data[i][5])
        doge.append(data[i][6])
        xrp.append(data[i][7])
        trx.append(data[i][8])
        time.append(i*3/60*-1)
    time.reverse()
    matplotlib.rcParams['axes.unicode_minus'] = False
    matplotlib.rcParams['font.family'] = "NanumGothicCoding"
    matplotlib.rcParams['figure.figsize'] = (7, 4)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    a = ax1.plot(time, btc, color='darkorange', label="비트코인")
    ax1.set_ylim([min(btc)-min(btc)/500, max(btc)+max(btc)/500])
    ax1.set_xlabel('시간 (h)')
    ax1.tick_params(axis='y', length=0, labelcolor='white')
    plt.title('시세 그래프', loc='right')
    ax2 = ax1.twinx()
    b = ax2.plot(time, eth, color='skyblue', label="이더리움")
    ax2.set_ylim([min(eth)-min(eth)/500, max(eth)+max(eth)/500])
    ax2.tick_params(axis='y', length=0, labelcolor='white')
    ax3 = ax2.twinx()
    c = ax3.plot(time, ltc, color='royalblue', label="라이트코인")
    ax3.set_ylim([min(ltc)-min(ltc)/500, max(ltc)+max(ltc)/500])
    ax3.tick_params(axis='y', length=0, labelcolor='white')
    ax4 = ax3.twinx()
    d = ax4.plot(time, dot, color='mediumvioletred', label="폴카닷")
    ax4.set_ylim([min(dot)-min(dot)/500, max(dot)+max(dot)/500])
    ax4.tick_params(axis='y', length=0, labelcolor='white')
    ax5 = ax4.twinx()
    e = ax5.plot(time, ada, color='midnightblue', label="에이다")
    ax5.set_ylim([min(ada)-min(ada)/500, max(ada)+max(ada)/500])
    ax5.tick_params(axis='y', length=0, labelcolor='white')
    ax6 = ax5.twinx()
    f = ax6.plot(time, doge, color='gold', label="도지코인")
    ax6.set_ylim([min(doge)-min(doge)/500, max(doge)+max(doge)/500])
    ax6.tick_params(axis='y', length=0, labelcolor='white')
    ax7 = ax6.twinx()
    g = ax7.plot(time, xrp, color='dimgrey', label="리플")
    ax7.set_ylim([min(xrp)-min(xrp)/500, max(xrp)+max(xrp)/500])
    ax7.tick_params(axis='y', length=0, labelcolor='white')
    ax8 = ax7.twinx()
    h = ax8.plot(time, trx, color='red', label="트론")
    ax8.set_ylim([min(trx)-min(trx)/500, max(trx)+max(trx)/500])
    ax8.tick_params(axis='y', length=0, labelcolor='white')
    lns = a+b+c+d+e+f+g+h
    labs = [l.get_label() for l in lns]
    leg = ax1.legend(lns, labs, loc=2, framealpha=0.7)
    leg.remove()
    ax8.add_artist(leg)
    plt.savefig('graph.png')
    fig.clf()
    plt.close()

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