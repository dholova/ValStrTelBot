import telebot
from telebot import types as tps
import os

bot = telebot.TeleBot('5254868393:AAEAKmPlIshuC5Zh1qfHwSnKr4CBUX5WmG8')


@bot.message_handler(commands=['start'])
def start(message):
    markup = tps.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    Smiris = tps.KeyboardButton('Смирись и расслабься')
    Chast = tps.KeyboardButton('Часть чего-то большего')
    Razvlecheniye = tps.KeyboardButton('Развлечение')
    markup.add(Smiris, Chast, Razvlecheniye)
    bot.send_message(message.chat.id, 'Привет, какой альбом хочешь послушать?)', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    albums = ["развлечение", "смирись и расслабься", "часть чего-то большего"]
    for album_name in albums:
        if message.text.lower() == album_name:
            album_name = album_name.lower()
            step = 1
            for song in os.listdir(f'./{album_name}'):
                audio = open(f'./{album_name}/{song}', 'rb')
                bot.send_message(message.chat.id, f'Отправляю песню {song}')
                current_id = message.message_id
                bot.send_audio(message.chat.id, audio, timeout=500)
                bot.delete_message(message.chat.id, message_id=current_id+step)
                step += 2  # delete comment messages
    if message.text.lower() not in albums:
        bot.send_message(message.chat.id, 'Я тебя не понимаю', parse_mode='html')


bot.polling(non_stop=True)
