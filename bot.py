from discord.ext import commands
import discord
import random
import time
import dotenv
import os
import datetime
import mysql.connector

dotenv.load_dotenv(dotenv.find_dotenv())

intents = discord.Intents.all()

prefix = "!"
bot = commands.Bot(command_prefix=prefix, intents=intents)


@bot.command()
async def load(ctx, extension):
    if ctx.author.id == int(os.environ["BOT_OWNER"]):
        bot.load_extension(f"commands.{extension}")
        await ctx.send("Бот загружен")
    else:
        await ctx.send("Загрузить бота может только лягушка")

@bot.command()
async def unload(ctx, extension):
    if ctx.author.id == int(os.environ["BOT_OWNER"]):
        bot.unload_extension(f"commands.{extension}")
        await ctx.send("Бот выгружен")
    else:
        await ctx.send("Выгрузить бота может только лягушка")

@bot.command()
async def reload(ctx, extension):
    if ctx.author.id == int(os.environ["BOT_OWNER"]):
        bot.unload_extension(f"commands.{extension}")
        bot.load_extension(f"commands.{extension}")
        await ctx.send("Бот перезагружен")
    else:
        await ctx.send("Перезагрузить бота может только лягушка")

for filename in os.listdir("./commands"):
    if filename.endswith(".py"):
        bot.load_extension(f"commands.{filename[:-3]}")

bot.run(os.environ["TOKEN"])