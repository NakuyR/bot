import discord
from discord.channel import VoiceChannel
from discord.ext import commands
from youtube_dl import YoutubeDL, options
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import time
import os

bot = commands.Bot(command_prefix='야 ')
client=discord.Client()

user=[]
musictitle=[]
song_queue=[]
musicnow=[]

def title(msg):
    global music

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    driver = load_chrome_driver()
    driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    music = entireNum.text.strip()
    
    musictitle.append(music)
    musicnow.append(music)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com'+test1
    with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']

    driver.quit()
    
    return music, URL

def play(ctx):
    global vc
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    URL = song_queue[0]
    del user[0]
    del musictitle[0]
    del song_queue[0]
    vc = get(bot.voice_clients, guild=ctx.guild)
    if not vc.is_playing():
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx)) 

def play_next(ctx):
    if len(musicnow) - len(user) >= 2:
        for i in range(len(musicnow) - len(user) - 1):
            del musicnow[0]
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if len(user) >= 1:
        if not vc.is_playing():
            del musicnow[0]
            URL = song_queue[0]
            del user[0]
            del musictitle[0]
            del song_queue[0]
            vc.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
    else:
        if not vc.is_playing():
            client.loop.create_task(vc.disconnect())        

def load_chrome_driver():
      
    options = webdriver.ChromeOptions()

    options.binary_location = os.getenv('GOOGLE_CHROME_BIN')

    options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    return webdriver.Chrome(executable_path=str(os.environ.get('CHROME_EXECUTABLE_PATH')), chrome_options=options) 

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("봇 연구"))

    if not discord.is_loaded():
        discord.opus.load_opus('opus')

@bot.command()
async def 따라하기(ctx, *, text):
    await ctx.send(text)

@bot.command()
async def 들어와(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        await ctx.send(embed = discord.Embed(title= "음성 채널", description = "음성 채널에 접속합니다.", color = 0x00ff00))
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send(embed = discord.Embed(title= "음성 채널", description = "음성 채널에 접속해서 명령어를 입력해주세요", color = 0x00ff00))

@bot.command()
async def 나가(ctx):
    try:
        await vc.disconnect()
        await ctx.send(embed = discord.Embed(title= "음성 채널", description = "음성 채널에서 나갑니다.", color = 0x00ff00))
    except:
        await ctx.send(embed = discord.Embed(title= "음성 채널", description = "현재 음성 채널에 들어가있지 않아요", color = 0x00ff00))
    
@bot.command()
async def URL재생(ctx, *, url):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        await ctx.send(embed = discord.Embed(title= "음성 채널", description = "음성 채널에 접속합니다.", color = 0x00ff00))
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send(embed = discord.Embed(title= "음성 채널", description = "음성 채널에 접속해서 명령어를 입력해주세요", color = 0x00ff00))

    YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + url + "을(를) 재생하고 있습니다.", color = 0x00ff00))
    else:
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "이미 노래가 재생 중이라 노래를 재생할 수 없어요!", color = 0x00ff00))

@bot.command()
async def 재생(ctx, *, msg):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        await ctx.send(embed = discord.Embed(title= "음성 채널", description = "음성 채널에 접속합니다.", color = 0x00ff00))
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send(embed = discord.Embed(title= "음성 채널", description = "음성 채널에 접속해서 명령어를 입력해주세요", color = 0x00ff00))    
    if not vc.is_playing():
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        driver = load_chrome_driver()
        driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl

        driver.quit()
        musicnow.insert(0, entireText) 

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),after=lambda e: play_next(ctx))
    else:
        user.append(msg)
        result, URLTEST = title(msg)
        song_queue.append(URLTEST)
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = result+"을(를) 대기열에 추가합니다.", color = 0x00ff00))

@bot.command()
async def 일시정지(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed = discord.Embed(title= "일시정지", description = musicnow[0] + "을(를) 일시정지 했습니다.", color = 0x00ff00))
    else:
        await ctx.send(embed = discord.Embed(title= "일시정지", description = "현재 노래가 재생되지 않고 있어요", color = 0x00ff00))

@bot.command()
async def 다시재생(ctx):
    try:
        vc.resume()
    except:
         await ctx.send(embed = discord.Embed(title= "다시재생", description = "현재 노래가 재생되지 않고 있어요", color = 0x00ff00))
    else:
         await ctx.send(embed = discord.Embed(title= "다시재생", description = musicnow[0]  + "을(를) 다시 재생했습니다.", color = 0x00ff00))

@bot.command()
async def 노래끄기(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed = discord.Embed(title= "노래끄기", description = musicnow[0]  + "을(를) 종료했습니다.", color = 0x00ff00))
    else:
        await ctx.send(embed = discord.Embed(title= "노래끄기", description = "현재 노래가 재생되지 않고 있어요", color = 0x00ff00))

@bot.command()
async def 현재노래(ctx):
    if not vc.is_playing():
        await ctx.send(embed = discord.Embed(title= "지금노래", description = "현재 노래가 재생되지 않고 있어요", color = 0x00ff00))
    else:
        await ctx.send(embed = discord.Embed(title = "지금노래", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))

@bot.command()
async def 멜론차트(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        await ctx.send(embed = discord.Embed(title= "음성 채널", description = "음성 채널에 접속합니다.", color = 0x00ff00))
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send(embed = discord.Embed(title= "음성 채널", description = "음성 채널에 접속해서 명령어를 입력해주세요", color = 0x00ff00))

    if not vc.is_playing():
        
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        driver = load_chrome_driver()
        driver.get("https://www.youtube.com/results?search_query=멜론차트")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl 

        driver.quit()

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "멜론차트", description = "현재 " + entireText + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        await ctx.send("이미 노래가 재생 중이라 노래를 재생할 수 없어요!")

@bot.command()
async def 대기열추가(ctx, *, msg):
    user.append(msg)
    result, URLTEST = title(msg)
    song_queue.append(URLTEST)
    await ctx.send(embed = discord.Embed(title= "대기열 추가", description = result + "를 재생목록에 추가했어요!", color = 0x00ff00))

@bot.command()
async def 대기열삭제(ctx, *, number):
    try:
        ex = len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number)-1]
        del musicnow[int(number)-1+ex]
        await ctx.send(embed = discord.Embed(title= "대기열 삭제", description = "대기열이 정상적으로 삭제되었어요", color = 0x00ff00))
    except:
        if len(list) == 0:
            await ctx.send(embed = discord.Embed(title= "대기열 삭제", description = "대기열에 노래가 없어요!", color = 0x00ff00))
        else:
            if len(list) < int(number):
                await ctx.send(embed = discord.Embed(title= "대기열 삭제", description = "대기열에 있는 수보다 많아요!", color = 0x00ff00))
            else:
                await ctx.send(embed = discord.Embed(title= "대기열 삭제", description = "숫자를 입력해주세요!", color = 0x00ff00))

@bot.command()
async def 대기열(ctx):
    if len(musictitle) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
            
        await ctx.send(embed = discord.Embed(title= "대기열", description = Text.strip(), color = 0x00ff00))

@bot.command()
async def 대기열초기화(ctx):
    try:
        ex = len(musicnow) - len(user)
        del user[:]
        del musictitle[:]
        del song_queue[:]
        while True:
            try:
                del musicnow[ex]
            except:
                break
        await ctx.send(embed = discord.Embed(title= "대기열초기화", description = """대기열이 정상적으로 초기화되었습니다.""", color = 0x00ff00))
    except:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")

@bot.command()
async def 명령어(ctx):
    await ctx.send(embed = discord.Embed(title='도움말',description="""
\n야 명령어 -> 봇의 모든 명령어를 볼 수 있습니다.
\n야 들어와 -> 봇을 자신이 속한 채널로 부릅니다.
\n야 나가 -> 뮤직봇을 자신이 속한 채널에서 내보냅니다.
\n야 URL재생 [노래링크] -> 유튜브URL를 입력하면 봇이 노래를 틀어줍니다.
(대기열에 추가할 수 없어요.)
\n야 재생 [노래이름] -> 봇이 노래를 검색해 틀어줍니다.
\n야 노래끄기 -> 현재 재생중인 노래를 끕니다.
야 일시정지 -> 현재 재생중인 노래를 일시정지시킵니다.
야 다시재생 -> 일시정지시킨 노래를 다시 재생합니다.
\n야 현재노래 -> 현재 재생되고 있는 노래의 제목을 알려줍니다.
\n야 멜론차트 -> 최신 멜론차트를 재생합니다.
\n야 대기열 -> 이어서 재생할 노래목록을 보여줍니다.
야 대기열초기화 -> 대기열에 추가된 모든 노래를 지웁니다.
야 대기열삭제 [숫자] -> 대기열에서 입력한 숫자에 해당하는 노래를 지웁니다.""", color = 0x00ff00))


bot.run('OTIwNjgxNTgyOTI5NTIyNzU4.Ybn5ig.FFP5vCQATm8jz4wiKvcOmETihDs')
