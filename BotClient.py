import discord
import os
from discord.ext import commands
from youtube_dl import YoutubeDL
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import time

bot = commands.Bot(command_prefix='껍질아 ')
client = discord.Client()

token_path = os.path.dirname(os.path.abspath(__file__))+"/LoadToken.txt"
t = open(token_path, "r", encoding="utf-8")
token = t.read().split()[0]

user = []
musictitle = []
song_queue = []
musicnow = []

def title(msg):
    global music

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    chromedriver_dir = r"C:\Users\Amondyoutube12\Downloads\Bot\Other\ChromeDriver\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_dir, options = options)
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

@bot.event
async def on_ready():
    print('Login')
    await bot.change_presence(status=discord.Status.online, activity=None)

@bot.command()
async def 따라해(ctx, *, text):
    await ctx.send(text)

@bot.command()
async def 입장(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("음성 채널에 입장할 수 없습니다. 사용자가 음성 채널에 입장해 있는지 확인해 주세요.")

@bot.command()
async def 퇴장(ctx):
    try:
        await vc.disconnect()
    except:
        await ctx.send("음성 채널을 퇴장할 수 없습니다. 봇이 음성 채널에 입장해 있는지 확인해 주세요.")

@bot.command()
async def 링크재생(ctx, *, url):
    
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("음성 채널에 입장할 수 없습니다. 사용자가 음성 채널에 입장해 있는지 확인해 주세요.")

    YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send(embed = discord.Embed(title= "음악 재생", description = "현재 " + url + " 을(를) 재생 중입니다.", color = 0x3498DB))
    else:
        await ctx.send("음악을 재생할 수 없습니다. 재생 중인 음악을 종료해 주세요")

@bot.command()
async def 재생(ctx, *, msg):
    
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("음성 채널에 입장할 수 없습니다. 사용자가 음성 채널에 입장해 있는지 확인해 주세요.")
    
    if not vc.is_playing():
        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        chromedriver_dir = r"C:\Users\Amondyoutube12\Downloads\Bot\Other\ChromeDriver\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir)
        driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl 

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "음악 재생", description = "현재 " + entireText + " 을(를) 재생 중입니다.", color = 0x3498DB))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        user.append(msg)
        result, URLTEST = title(msg)
        song_queue.append(URLTEST)
        await ctx.send(result + " 을(를) 재생 목록에 추가시켰습니다.")

@bot.command()
async def 정지(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed = discord.Embed(title= "일시 정지", description = musicnow[0] + "을(를) 일시 정지 하였습니다.", color = 0x3498DB))
    else:
        await ctx.send("음악을 정지할 수 없습니다. 음악이 재생 중인지 확인해 주세요.")

@bot.command()
async def 재시작(ctx):
    try:
        vc.resume()
    except:
         await ctx.send("음악을 재시작할 수 없습니다. 음악이 재생 중인지 확인해 주세요.")
    else:
         await ctx.send(embed = discord.Embed(title= "재시작", description = musicnow[0]  + "을(를) 다시 재생했습니다.", color = 0x3498DB))

@bot.command()
async def 종료(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed = discord.Embed(title= "음악 종료", description = musicnow[0]  + "을(를) 종료했습니다.", color = 0x3498DB))
    else:
        await ctx.send("음악을 종료할 수 없습니다. 음악이 재생 중인지 확인해 주세요.")

@bot.command()
async def 음악(ctx):
    if not vc.is_playing():
        await ctx.send("음악 정보를 불러올 수 없습니다. 음악이 재생 중인지 확인해 주세요.")
    else:
        await ctx.send(embed = discord.Embed(title = "재생 중인 음악", description = "현재 " + musicnow[0] + " 을(를) 재생 중입니다.", color = 0x3498DB))

@bot.command()
async def 차트(ctx):
    if not vc.is_playing():
        
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        chromedriver_dir = r"C:\Users\Amondyoutube12\Downloads\Bot\Other\ChromeDriver\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir, options = options)
        driver.get("https://www.youtube.com/results?search_query=멜론차트")
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
        await ctx.send(embed = discord.Embed(title= "음악 재생", description = "현재 " + entireText + " 을(를) 재생 중입니다.", color = 0x3498DB))
        vc.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
    else:
        await ctx.send("음악을 재생할 수 없습니다. 재생 중인 음악을 종료해 주세요.")

@bot.command()
async def 목록추가(ctx, *, msg):
    user.append(msg)
    result, URLTEST = title(msg)
    song_queue.append(URLTEST)
    await ctx.send(result + " 을(를) 재생 목록에 추가하였습니다.")

@bot.command()
async def 목록삭제(ctx, *, number):
    try:
        ex = len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number)-1]
        del musicnow[int(number)-1+ex]
            
        await ctx.send("음악을 재생 목록에서 삭제하였습니다.")
    except:
        if len(list) == 0:
            await ctx.send("재생 목록을 삭제할 수 없습니다. 음악이 추가되어 있는지 확인해 주세요.")
        else:
            if len(list) < int(number):
                await ctx.send("음악을 재생 목록에서 삭제할 수 없습니다. 입력한 번호가 음악의 번호와 일치하는지 확인해 주세요.")
            else:
                await ctx.send("음악을 삭제할 수 없습니다. 삭제할 음악의 번호를 입력하였는지 확인해 주세요.")

@bot.command()
async def 목록(ctx):
    if len(musictitle) == 0:
        await ctx.send("정보를 불러오지 못하였습니다. 재생 목록에 음악이 추가되어 있는지 확인해 주세요.")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
            
        await ctx.send(embed = discord.Embed(title= "음악 재생 목록", description = Text.strip(), color = 0x3498DB))

@bot.command()
async def 목록리셋(ctx):
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
        await ctx.send(embed = discord.Embed(title= "재생 목록 초기화", description = """재생 목록 초기화를 완료하였습니다.""", color = 0x3498DB))
    except:
        await ctx.send("재생 목록을 초기화할 수 없습니다. 재생 목록에 음악이 추가되어 있는지 확인해 주세요.")

@bot.command()
async def 목록재생(ctx):

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    if len(user) == 0:
        await ctx.send("재생 목록을 재생할 수 없습니다. 재생 목록에 음악이 추가되어 있는지 확인해 주세요.")
    else:
        if len(musicnow) - len(user) >= 1:
            for i in range(len(musicnow) - len(user)):
                del musicnow[0]
        if not vc.is_playing():
            play(ctx)
        else:
            await ctx.send("재생 목록이 이미 재생 중입니다.")

bot.run(token)