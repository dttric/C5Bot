from discord.ext import commands
import discord
import random
import time
import dotenv
import os
import datetime
import json

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Экономические команды загружены")
        
def setup(bot):
    bot.add_cog(Economy(bot))