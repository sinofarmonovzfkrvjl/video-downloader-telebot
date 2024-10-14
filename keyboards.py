from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_audio() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="ovozini yuklash", callback_data="download_voice")
    )

    return keyboard

def get_audio2() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="ovozini yuklash", callback_data="download_voice2")
    )