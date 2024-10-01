import telebot
import requests
import glob
from os import remove
from downloader import VideoDownloader, InstagramDownloader

API_TOKEN = "7307034091:AAHS8DnWDo4aJaxLu_0jd3hZkRR5Lm-Xvdg"

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_message(message.chat.id, f"Salom {message.from_user.full_name}\nmen youtube va instagramdan video yuklovchi botman")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith(("https://youtube.com/", "https://www.youtube.com/", "https://youtu.be/", 
                                "https://tiktok.com/", "https://www.tiktok.com/", "https://www.facebook.com/", 
                                "https://www.facebook.com")):
        bot.send_message(message.chat.id, "Video yuklanmoqda...")
        video = VideoDownloader(message.text)
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
        response = requests.get(downloaded['url'])

        if message.text.startswith("https://www.instagram.com/p/"):
            with open("image.png", "wb") as f:
                f.write(response.content)
            try:
                bot.send_photo(message.chat.id, open("image.png", 'rb'))
                bot.send_message(message.chat.id, downloaded['description'])
            except Exception as e:
                bot.send_message(message.chat.id, f"Xatolik: {str(e)}")
            finally:
                remove("image.png")

        elif message.text.startswith("https://www.instagram.com/reel/"):
            with open("video.mp4", "wb") as f:
                f.write(response.content)
            try:
                bot.send_video(message.chat.id, open("video.mp4", 'rb'))
                bot.send_message(message.chat.id, downloaded['description'])
            except Exception as e:
                bot.send_message(message.chat.id, "Videoni yuklab bo'lmadi")
            finally:
                remove("video.mp4")


if __name__ == '__main__':
    print(f"[@{bot.get_me().username}] '{bot.get_me().full_name}' is started!")
    bot.polling(none_stop=True)
