from telebot import TeleBot, types
import requests
from os import remove
from dotenv import load_dotenv
from keyboards import get_audio, get_audio2
import os

load_dotenv()

API_TOKEN = str(os.getenv("API_TOKEN"))
bot = TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def command_start(message: types.Message):
    bot.send_message(message.chat.id, f"Salom {message.from_user.full_name}\nmen youtube va instagramdan video yuklovchi botman")

@bot.message_handler(commands=['settoken'])
def set_token(message: types.Message):
    if message.from_user.id == 7077167971:
        if len(message.text.split()) < 2:
            bot.send_message(message.chat.id, "Iltimos tokenini kiriting")
        elif len(message.text.split()) == 2:
            with open("token.txt", "w") as f:
                f.write(message.text.split()[1])
            bot.send_message(message.chat.id, "Token muvaffaqiyatli o'zgartirildi")
    else:
        bot.send_message(message.chat.id, "Siz tokenni o'zgartiraolmaysiz")

@bot.message_handler(func=lambda message: True)
def handle_message(message: types.Message):
    global response
    bot.send_message(message.chat.id, "Video yuklanmoqda...")
    token = open("token.txt", "r").read()
    if message.text.startswith(("https://www.instagram.com/reel/", "https://www.instagram.com/p/")):
        response = requests.get("https://full-media-downloader-pro-zfkrvjl323.onrender.com/instagram1", params={"url": message.text, "token": token})

        if response.status_code == 200:
            if response.json()['type'] == "Image":    
                bot.send_photo(message.chat.id, response.json()['url'])

            elif response.json()['type'] == "Video":
                bot.send_video(message.chat.id, response.json()['url'])

            elif response.json()['type'] == "Album":
                for url in response.json()['url']:
                    bot.send_photo(message.chat.id, url)
            else:
                bot.send_message(message.chat.id, "Videoni yuklab bo'lmadi")
            bot.send_message(message.chat.id, f"Profile: {response.json()['Profile']}\nCaption: {response.json()['Caption']}")
        else:
            bot.send_message(message.chat.id, "Videoni yuklab bo'lmadi")

    elif message.text.startswith(("https://www.youtube.com/watch?v=", "https://youtu.be/")):
        bot.send_message(message.chat.id, "Video yuklanmoqda...")
        print("Video yuklanmoqda...")
        response = requests.get("https://full-downloader-api-zfkrvjl323.onrender.com/youtube1", params={"url": message.text, "token": token})
        print("passed the response")
        if response.status_code == 200:
            print("passed the status code")
            try:
                print(response.json()['qualities'][0]['url'])
                bot.send_video(message.chat.id, response.json()['qualities'][0]['url'], caption=response.json()['metaInfo']['title'], reply_markup=get_audio())
            except:
                response = requests.get("https://full-downloader-api-phi.vercel.app/youtube2", params={"url": message.text, "token": token})
                try:
                    print(response.json()['data']['videos'][0]['url'])
                    bot.send_video(message.chat.id, response.json()['data']['videos'][0]['url'], caption=response.json()['data']['info']['title'], reply_markup=get_audio2())
                except:
                    try:
                        bot.send_video(message.chat.id, response.json()['data']['videos'][0]['url'])
                    except:
                        bot.send_message(message.chat.id, "Videoni yuklab bo'lmadi")
        else:
            print("ERROR: " + response.status_code)

@bot.callback_query_handler(func=lambda call: call.data == "download_voice")
def send_audio(message: types.Message):
    print(response.json()['qualities'][2]['url'])
    bot.send_audio(message.chat.id, response.json()['qualities'][2]['url'])

@bot.callback_query_handler(func=lambda call: call.data == "download_voice2")
def send_audio(message: types.Message):
    print(response.json()['qualities'][2]['url'])
    bot.send_audio(message.chat.id, response.json()['qualities'][2]['url'])


bot.delete_webhook()
print(f"[@{bot.get_me().username}] - '{bot.get_me().full_name}' started!")
bot.infinity_polling(timeout=False, long_polling_timeout=False)