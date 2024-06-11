import discord
from discord.ext import commands
import psycopg2
from datetime import datetime
import re
from dotenv import load_dotenv
import os
from src.database.index import connectDB
from src.libs.discord.sendMessage import sendMessage

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=os.getenv("PREFIX"), intents=intents)

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

@bot.command()
async def buy(ctx, *, command):
    if ctx.channel.id != CHANNEL_ID:
        return

    account_match = re.search(r"Account:\s*\[(.*?)\]", command, re.IGNORECASE)
    character_match = re.search(r"Character:\s*\[(.*?)\]", command, re.IGNORECASE)
    item_id_match = re.search(r"Item ID:\s*\[(.*?)\]", command, re.IGNORECASE)
    amount_match = re.search(r"Amount:\s*\[(.*?)\]", command, re.IGNORECASE)

    if not account_match or not character_match or not item_id_match or not amount_match:
        await sendMessage(bot, CHANNEL_ID, "Incorrect command format.")
        return

    account = account_match.group(1)
    character = character_match.group(1)
    item_id = item_id_match.group(1)
    amount = amount_match.group(1)
 
    try:
        connection = connectDB(os.getenv("BUY_DB_NAME"))
        cursor = connection.cursor()
        cursor.execute("""
                       INSERT INTO item_receivable 
                          (account_name, item_id, item_quantity, world_id, 
                            player_name, point, amount, mail_name, money_type) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                       """,
                       (account, item_id, amount, 1010, character, 1, amount, '', 1))
        connection.commit()
        cursor.close()
        connection.close()
        await sendMessage(bot, CHANNEL_ID, f"Sent: {amount} items with ID:{item_id} to account:{account}")
    except Exception as e:
        print("Error updating the database:", e)
        await sendMessage(bot, CHANNEL_ID, "There was an error updating the database.")

@bot.command()
async def addPoints(ctx, *, command):
    if ctx.channel.id != CHANNEL_ID:
        return

    account_match = re.search(r"Account:\s*\[(.*?)\]", command, re.IGNORECASE)
    points_match = re.search(r"Points:\s*\[(.*?)\]", command, re.IGNORECASE)

    if not account_match or not points_match:
        await sendMessage(bot, CHANNEL_ID, "Incorrect command format.")
        return

    account = account_match.group(1)
    points = points_match.group(1)
 
    try:
        connection = connectDB(os.getenv("ADD_POINTS_DB_NAME"))
        cursor = connection.cursor()
        sql = """UPDATE tb_user SET pvalues = pvalues + %s WHERE mid = %s"""
        cursor.execute(sql, (points, account))
        connection.commit()
        cursor.close()
        connection.close()
        await sendMessage(bot, CHANNEL_ID, f"Added: {points} points to user: {account}")
    except Exception as e:
        print("Error updating the database:", e)
        await sendMessage(bot, CHANNEL_ID, "There was an error updating the database.")

@bot.command()
async def addBonus(ctx, *, command):
    if ctx.channel.id != CHANNEL_ID:
        return

    account_match = re.search(r"Account:\s*\[(.*?)\]", command, re.IGNORECASE)
    bonus_match = re.search(r"Bonus:\s*\[(.*?)\]", command, re.IGNORECASE)

    if not account_match or not bonus_match:
        await sendMessage(bot, CHANNEL_ID, "Incorrect command format.")
        return

    account = account_match.group(1)
    bonus = bonus_match.group(1)
 
    try:
        connection = connectDB(os.getenv("ADD_BONUS_DB_NAME"))
        cursor = connection.cursor()
        sql = """UPDATE tb_user SET bonus = bonus + %s WHERE mid = %s"""
        cursor.execute(sql, (bonus, account))
        connection.commit()
        cursor.close()
        connection.close()
        await sendMessage(bot, CHANNEL_ID, f"Added: {bonus} bonus to user: {account}")
    except Exception as e:
        print("Error updating the database:", e)
        await sendMessage(bot, CHANNEL_ID, "There was an error updating the database.")

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
