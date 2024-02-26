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
        
    @commands.command()
    async def regineco(self, ctx, id, type):
        def check_user(db, id):
            return id in db
        if type not in range(1, 3):
            ctx.send("Типы нумеруются от 1 до 3.\n1 - Страна-Мажор\n2 - Обычная страна\n3 - Страна третьего мира.")
                
        else:
            with open("db.json") as database:
                database_object = json.load(database)
            
            active_db = json.dumps(database_object)
                
            new_user = {
                "user": id,
                "balance": 0,
                "type": type
            }
                
            if check_user(database_object, id) == True:
                await ctx.send("Пользователь был зарегистрирован в системе экономики.")
            else:
                new_db = {**active_db, **new_user}
                with open("db_backup.json", "w") as database:
                    json.dump(new_db, database)
                with open("db.json", "w") as database:
                    json.dump(new_db, database)
            
        
    @commands.command()
    async def add_money(self, ctx, id, addmoney):
        pass
    
    @commands.command()
    async def bal(self, ctx):
        pass
        
def setup(bot):
    bot.add_cog(Economy(bot))