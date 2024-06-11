import discord
from discord.ext import commands
import psycopg2
from datetime import datetime
import re
from dotenv import load_dotenv
import os

load_dotenv()
def connectDB(database):
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=database,
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return connection
    except psycopg2.Error as e:
        print(e)
