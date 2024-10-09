from telebot import TeleBot, types
import requests
import glob
from os import remove
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = str(os.getenv("API_TOKEN"))
bot = TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def command_start(message: types.Message):
    bot.send_message(message.chat.id, f"Salom {message.from_user.full_name}\nmen youtube va instagramdan video yuklovchi botman")

@bot.message_handler(func=lambda message: True)
def handle_message(message: types.Message):
    if message.text.startswith(("https://www.instagram.com/reel/", "https://www.instagram.com/p/")):
        response = requests.get("https://full-downloader-api-zfkrvjl323.onrender.com/instagram", params={"url": message.text})
        