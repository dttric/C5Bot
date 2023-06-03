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


intents = discord.Intents.all()
# cursor = connection.cursor()
prefix = "!"
bot = commands.Bot(command_prefix=prefix, intents=intents)


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

@bot.command()
async def referend(ctx, *values):
    if ctx.channel.id != 1068947402398105651:
        embed = discord.Embed(title="Ошибка", description="Доступно только в <#1068947402398105651>", color=0xff0000)
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

@bot.command()
async def cal(ctx, *values):
    evaled = int(eval(" ".join(values)))
    if evaled == False:
        evaled = "Неверно"
    elif evaled == True:
        evaled = "Верно"
    embed=discord.Embed(title="Калькулятор", description=evaled, color=0xff0000)
    await ctx.send(embed=embed)

@bot.command()
async def e(ctx, *values):
    if ctx.author.id == int(os.environ["BOT_OWNER"]):
        evaled = eval(" ".join(values))
        embed=discord.Embed(title="!eval", description=evaled, color=0xff0000)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Ошибка!", description="Ты не владелец бота", color=0xff0000)
        await ctx.send(embed=embed)

@bot.command()
async def create_item(ctx, arg1, arg2, arg3):
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

@bot.command()
async def buy(ctx, item):
    # Check if the user has enough balance
    cursor = connection.cursor()
    cursor.execute("""
    SELECT balance FROM users WHERE username = %s
    """, (ctx.author.name,))
    balance = cursor.fetchone()[0]

    if balance < item.price:
        await ctx.send("У вас нет денег")
        return
    
    # Update the user's balance
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE users SET balance = balance - %s WHERE username = %s
    """, (item.price, ctx.author.name))
    connection.commit()
    cursor.close()

    # Add the item to the user's inventory
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO inventory (user_id, item_id, count) VALUES
    (%s, %s, 1)
    """, (ctx.author.id, item.id))
    connection.commit()
    cursor.close()

    # Send a message to the user
    await ctx.send("Ты купил {}.".format(item.name))
    cursor.close()

bot.run(os.environ["TOKEN"])