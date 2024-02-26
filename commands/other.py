from discord.ext import commands
import discord
import random
import time
import dotenv
import os
import datetime

class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(" \"Другие\" команды загружены")

    @commands.command()
    async def referend(self, ctx, *values):
        if ctx.channel.id != 1211195657390522410:
            embed = discord.Embed(title="Ошибка", description="Доступно только в <#1211195657390522410>", color=0xff0000)
            await ctx.send(embed=embed)
        elif values == "":
            embed = discord.Embed(title="Ошибка", description="Введите тему референдума", color=0xff0000)
            await ctx.send(embed=embed)
        else:
            sogl = random.randint(1, 100)
            nesogl = random.randint(1, 100 - sogl)
            yavka = 100 - (sogl + nesogl)
            embed=discord.Embed(title=" ".join(values), color=0x29657f)
            embed.add_field(name="Согласны", value=f"{sogl}%", inline=False)
            embed.add_field(name="Не согласны", value=f"{nesogl}%", inline=False)
            embed.add_field(name="Не пришли", value=f"{yavka}%", inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    async def e(self, ctx, *values):
        if ctx.author.id == int(os.environ["BOT_OWNER"]):
            evaled = eval(" ".join(values))
            embed=discord.Embed(title="!eval", description=evaled, color=0xff0000)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Ошибка!", description="Ты не владелец бота", color=0xff0000)
            await ctx.send(embed=embed)
            
    @commands.command(description="Создает красивый шаблон, чтобы не писать вручную.")
    async def шаблон(self, ctx):
        await ctx.respond("понг")
    
def setup(bot):
    bot.add_cog(Other(bot))