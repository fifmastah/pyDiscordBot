import json
import pyshorteners
import requests
import discord
from random_word import RandomWords
from discord.ext import commands
from discord.ext import tasks
from youtube_search import YoutubeSearch

intents = discord.Intents.default()
intents.members = True

client = discord.Client()

bot = commands.Bot(command_prefix='$', intents=intents)

shorten = pyshorteners.Shortener()

def parse_gif(gifSpec):
    ind = gifSpec.index(' ')
    spec = gifSpec[ind+1:]
    return spec

@bot.command(name='gif', help='sends a specific nanogif to the chat. Use by typing $gif followed by a space and then your desired gif')
async def gif(ctx, arg):
    r = requests.get(f'https://g.tenor.com/v1/search?q={arg}&key=YYXOKS2HN16V&limit=8')
    r = json.loads(r.content)
    await ctx.send(r['results'][0]['media'][0]['nanogif']['url'])

@bot.command(name='rgif')
async def r_gif(ctx, *arg):
    word = RandomWords()
    word = word.get_random_word()
    r = requests.get(f'https://g.tenor.com/v1/search?q={word}&key=YYXOKS2HN16V&limit=8')
    r = json.loads(r.content)
    await ctx.send(r['results'][0]['media'][0]['nanogif']['url'])
@bot.command(name='quote')
async def quote(ctx, *arg):
    r = requests.get('https://api.quotable.io/random')
    r = json.loads(r.content)
    author = r['author']
    unstring = '**' + r['content'] + '**' + f'\n- _{author}_'
    await ctx.send(unstring)
@bot.command(name='search')
async def search(ctx, arg):
    v_coll = YoutubeSearch(arg, max_results=5).to_dict()
    v_link = 'https://www.youtube.com/' + v_coll[0]['url_suffix']
    await ctx.send(v_link)
@tasks.loop(hours=24)
async def daily_times():
    channel =  bot.get_channel(788885978651033654)
    nyt_key = 'It6Tzec4rW3M2wdG1X2bmBCa9Uz3NGZq'
    r = requests.get(f'https://api.nytimes.com/svc/mostpopular/v2/emailed/7.json?api-key={nyt_key}')
    r = json.loads(r.content)
    if channel is not None:
        for i in range(5):
            title = r['results'][i]['title']
            author = r['results'][i]['byline']
            pre_short = r['results'][i]['url']
            shortened = shorten.tinyurl.short(f'{pre_short}')
            await channel.send('_TOP EMAILED STORIES OF THE DAY_\n' + '**' + title + '**' +  '\n'+ author + '\n' + shortened)
@bot.command(name='muteAll')
async def muteAll(ctx, *arg):
    for guild in bot.guilds:
        for member in guild.members:
            await member.edit(mute=True)
@bot.command(name='mute')
async def mute(ctx, *arg):
    for guild in bot.guilds:
        for member in guild.members:
            member_nick = str(member.nick).lower()
            for name in arg:
                name = name.lower()
                if name in member_nick:
                    await member.edit(mute=True)
@bot.command(name='unmute')
async def unmute(ctx, *arg):
    for guild in bot.guilds:
        for member in guild.members:
            member_nick = str(member.nick).lower()
            for name in arg:
                name = name.lower()
                if name in member_nick:
                    await member.edit(mute=False)



daily_times.start()
bot.run('ODcwNDk2MjIyMzI5MzA3MTQ3.YQNmyA.fraWWob2z0bz2h_cJy145QPXnuc')
