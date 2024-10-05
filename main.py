from telebot import TeleBot, types
import requests
import glob
from os import remove
from downloader import VideoDownloader, InstagramDownloader
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
    global video
    if message.text.startswith(("https://youtube.com/", "https://www.youtube.com/", "https://youtu.be/", 
                                "https://tiktok.com/", "https://www.tiktok.com/", "https://www.facebook.com/", 
                                "https://www.facebook.com")):
        global video
        bot.send_message(message.chat.id, "Video yuklanmoqda...")
        try:
            global video
            video = VideoDownloader(message.text)
        except:
            pass
        try:
            if video:
                video_file = glob.glob("*.mp4")[0]
                video_info = f"Video nomi: {video.get('title')}\n" \
                             f"Video yuklagan shaxs: {video.get('uploader')}\n" \
                             f"Layklar soni: {video.get('like_count')}\n" \
                             f"Dislayklar soni: {video.get('dislike_count')}\n" \
                             f"Ko'rishlar soni: {video.get('view_count')}\n" \
                             f"Video yuklangan sana: {video.get('upload_date')}"
                bot.send_video(message.chat.id, open(video_file, 'rb'), caption=video_info)
                bot.send_message(message.chat.id, f"Video izohi: {video.get('description')}")
            else:
                bot.send_message(message.chat.id, "Video yuklayolmadim")
        except Exception as e:
            bot.send_message(message.chat.id, f"Xatolik: {str(e)}")
        finally:
            remove(glob.glob("*.mp4")[0])

    elif message.text.startswith(("https://www.instagram.com/", "https://instagram.com/")):
        bot.send_message(message.chat.id, "Video yuklanmoqda...")
        downloaded = InstagramDownloader(message.text)
        if downloaded['type'] == "Video":
            try:
                bot.send_video(message.chat.id, downloaded['url'], caption=downloaded['Caption'])
            except:
                bot.send_video(message.chat.id, downloaded['url'])
                bot.send_message(message.chat.id, downloaded['Caption'])
        elif downloaded['type'] == "Image":
            try:
                bot.send_photo(message.chat.id, downloaded['url'], caption=downloaded['Caption'])
            except:
                bot.send_photo(message.chat.id, downloaded['url'])
                bot.send_message(message.chat.id, downloaded['Caption'])
        else:
            bot.send_message(5230484991, downloaded)

def process_update(update):

    bot.process_new_updates([update])


# if __name__ == '__main__':
#     print(f"[@{bot.get_me().username}] '{bot.get_me().full_name}' is started!")
#     bot.polling(none_stop=True, skip_pending=True, )
