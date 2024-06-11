from src.libs.discord.bot import bot
from dotenv import load_dotenv
import os
from src.database.index import connectDB
from src.libs.discord.sendMessage import sendMessage

load_dotenv()
bot.run(os.getenv("TOKEN"))
