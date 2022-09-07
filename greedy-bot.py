# greedy-bot.py
import os
import discord
from dotenv import load_dotenv
import asyncio
import random
from discord.ext import commands
import requests, json

#have the discord bot token in a .env file to hide it
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()
bot = commands.Bot(command_prefix="!")


#shows the bot connected to server
@bot.event 
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    #channel = client.get_channel(755168040546599017)
    #await channel.send("```Greedy-bot Online```")


#--deprecated--
#attempt to make a team choosing system based on captains or random
@client.event
async def on_message(message):
    if message.content.startswith("!team"):
        channel = message.channel
        await message.channel.send("""```Which mode would you like?
    1) Captain
    2) Random
    3) Manual```""")


#test command to see if bot is active    
@bot.command() 
async def test(ctx):
    await ctx.channel.send("```Hello World!```")

    
#rolling a dice in DnD/dice notation format
@bot.command()
async def roll(ctx, arg: str): 
    sum = 0
    if "d" in arg:
        dice = arg.split('d')
        dice = list(map(int, dice))
        rolls = [None] * dice[0]
        for j in range(dice[0]):
            rolls[j] = random.randint(1,dice[1])
            sum = (sum + rolls[j])
        rolls_formatted = (' + '.join(map(str,rolls)))
        await ctx.channel.send(f"```{sum}: {rolls_formatted}```")
    else: 
        await ctx.channel.send("```Please format in standard dice notation - 2d8 for 2, 8-sided dice```")


#flips a coin
@bot.command() 
async def flip(ctx):
    x = random.randint(1,2)
    if x == 1:
        await ctx.channel.send("```Heads```")
    else:
        await ctx.channel.send("```Tails```")


#defines a word
@bot.command(aliases=['def']) 
async def define(ctx, word: str, num: int):
    url = ("https://api.dictionaryapi.dev/api/v2/entries/en/" + word)
    data = requests.get(url, verify=False)
    #turn the data recieved from the API into JSON for easier parsing of word, definition, pos
    data_readable = data.json()
    word = data_readable[0]["word"]
    definition = data_readable[0]["meanings"][0]["definitions"][num - 1]["definition"]
    part_of_speech = data_readable[0]["meanings"][0]["partOfSpeech"]

    await ctx.channel.send(f"""```{word} 
({part_of_speech})
{num}. {definition}```""") 


#counts the number of instances a word was said by specific person
@bot.command(aliases=['wordcount'])
async def wc(ctx, name: discord.Member, word):
    counter = 0
    #have to limit at 5000 to avoid bot timing out
    messages = await ctx.history(limit = 5000).flatten()
    for message in messages:
        #avoid counting the word in the command
        if(message.author == name and not (message.content).startswith("!wc")):
            if word in message.content:
                counter += 1
    await ctx.channel.send(f"{name} said {word} {counter} times!")


bot.run(TOKEN)