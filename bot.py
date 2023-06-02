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

@bot.command()
async def referend(ctx, *values):
    if ctx.channel.id != 1068947402398105651:
        await ctx.send("Доступно только в <#1068947402398105651>")
    else:
        sogl = random.randint(1, 100)
        nesogl = random.randint(1, 100 - sogl)
        yavka = 100 - (sogl + nesogl)
        embed=discord.Embed(title=" ".join(values), color=0x29657f)
        embed.add_field(name="Согласны", value=f"{sogl}%", inline=False)
        embed.add_field(name="Не согласны", value=f"{nesogl}%", inline=False)
        embed.add_field(name="Не пришли", value=f"{yavka}%", inline=False)
        await ctx.send(embed=embed)
bot.run(os.environ.get("TOKEN"))