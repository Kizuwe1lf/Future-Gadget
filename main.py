import json
import random
from gtts import gTTS
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from secrets import bot_token


"""
   Hey you need ffmpeg to run it

   im not adding classic bot stuff there i just needed tts so i just coded it if u wanna add some cool stuff you can check my other bot it has some cool stuff to manage bot servers etc 

"""

def get_prefix(ctx, message):
    with open(r'prefixes.json', 'r') as f:
        prefixes = json.load(f)
    try:
        return prefixes[str(message.guild.id)]
    except:
        return '!'


bot = commands.Bot(command_prefix=get_prefix)



@bot.command()
@has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    prefixes = {}
    prefixes[str(ctx.guild.id)] = prefix
    with open(r'prefixes.json', 'a') as f:
        json.dump(prefixes, f)
    await ctx.send(f"Done new prefix = '{prefix}' for {ctx.guild.name} from now on")


@bot.command()
@has_permissions(administrator=True)
async def setlanguage(ctx, language):
    with open(r'language.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = language
    with open(r'language.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send(f"Done new tts language is '{language}' for {ctx.guild.name} from now on")


@bot.command() # before using join make sure you are connected to voice channel // only admins can make bot connect so theres no trolls
@has_permissions(administrator=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command() # only admins can make bot disconnect so theres no trolls
@has_permissions(administrator=True)
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command(aliases=['texttospeech']) # before using tts make sure bot is connected to voice_channel
async def tts(ctx, *message):

    # getting language if its exists
    with open(r'language.json', 'r') as f:
        languages = json.load(f)
    if str(ctx.guild.id) in languages.keys():
        language = languages[str(ctx.guild.id)]
    else:
        language = "tr"
    
    # geting text from tuple
    text = ""
    for word in message: 
        text += f"{word} "
        
    # getting soundfile
    soundfile = gTTS(text=text, lang=language, slow=False)
    
    # path is randomized cause its fun to check SoundFiles folder when files are stored random XD
    path = random.randint(1, 1000000000000)
    soundfile.save(f"SoundFiles/{path}.mp3")
    
    # play audio stuff
    guild = ctx.guild
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
    audio_source = discord.FFmpegPCMAudio(f"SoundFiles/{path}.mp3")
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)
        
bot.run(bot_token)
