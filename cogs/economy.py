from discord.ext import commands
import discord
import random
import time
import dotenv
import os
import datetime
import mysql.connector

dotenv.load_dotenv(dotenv.find_dotenv())

connection = mysql.connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DB_DATABASE"],
)
# !!!ЭТО РАСКОММЕНТИРОВАТЬ ТОЛЬКО НА ПЕРВЫЙ ЗАПУСК БОТА!!!

# cursor = connection.cursor()
# cursor.execute("""
# CREATE TABLE users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     balance INT NOT NULL
# )
# """)

# cursor.execute("""
# CREATE TABLE inventory (
#     user_id INT NOT NULL,
#     item_id INT NOT NULL,
#     count INT NOT NULL
# )
# """)

# cursor.execute("""
# CREATE TABLE shop (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     price INT NOT NULL,
#     role INT NOT NULL
# )
# """)
# cursor.close()

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Экономика загружена")
    
    @commands.command()
    async def create_item(self, ctx, arg1, arg2, arg3):
        cursor = connection.cursor()
        cursor.execute(f"""
        INSERT INTO shop (name, price, role) VALUES
        ('{arg1}', {arg2}, {arg3})
        """)
        
        connection.commit()
        cursor.close()
        embed=discord.Embed(title="Магазин", description=f"Предмет {arg1} успешно создан", color=0x1499d2)
        embed.set_footer(text=datetime.datetime)
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, item):
        cursor = connection.cursor()
        cursor.execute("""
        SELECT balance FROM users WHERE username = %s
        """, (ctx.author.name,))
        balance = cursor.fetchone()[0]

        if balance < item.price:
            await ctx.send("У вас нет денег")
            return
        
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE users SET balance = balance - %s WHERE username = %s
        """, (item.price, ctx.author.name))
        connection.commit()
        cursor.close()

        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO inventory (user_id, item_id, count) VALUES
        (%s, %s, 1)
        """, (ctx.author.id, item.id))
        connection.commit()
        cursor.close()

        await ctx.send("Ты купил {}.".format(item.name))
        cursor.close()

def setup(bot):
    bot.add_cog(Economy(bot))