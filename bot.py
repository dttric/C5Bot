from discord.ext import commands
import discord
import random
import time
import dotenv
import os
import datetime

dotenv.load_dotenv(dotenv.find_dotenv())

intents = discord.Intents.all()

prefix = "!"
bot = commands.Bot(command_prefix=prefix, intents=intents)

guild = bot.get_guild(int(os.environ["GUILD_ID"]))

@bot.event
async def on_ready():
    print(f"Я это {bot.user}")
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Project C5"))
        
@bot.command()
async def shutdown(ctx):
    if ctx.author.id == int(os.environ["BOT_OWNER"]):
        await ctx.send("Пока...")
        await bot.logout()
    else:
        await ctx.send("Так может только лягушка.")
        

@bot.command()
async def restart(ctx):
    if ctx.author.id == int(os.environ["BOT_OWNER"]):
        await bot.close()
        await bot.start(os.environ["TOKEN"])
        await ctx.send("Доброго утра! Пусть день сложится удачно!")
    else:
        await ctx.send("Так может только лягушка.")

for filename in os.listdir("./commands"):
    if filename.endswith(".py"):
        bot.load_extension(f"commands.{filename[:-3]}")

bot.run(os.environ["TOKEN"])