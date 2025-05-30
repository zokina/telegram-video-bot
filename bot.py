
from telebot import types
import os
import telebot
from flask import Flask, request
import time

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

video_path = "video.mp4"

# Главное меню — только одна кнопка
def main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🎥 Смотреть видео")
    bot.send_message(
        chat_id,
        'Первые шаги на пути к свободному танцу от директора школы ЭТО Александра Могилева. Смотри видео!',
        reply_markup=markup
    )

# /start
@bot.message_handler(commands=["start"])
def handle_start(message):
    main_menu(message.chat.id)

# Обработка кнопки "Смотреть видео"
@bot.message_handler(func=lambda message: message.text == "🎥 Смотреть видео")
def handle_video(message):
    chat_id = message.chat.id
    send_video_sequence(chat_id)
    time.sleep(180)  # Ждём 3 минуты

    # Кнопки-ссылки (Inline)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🌐 Наш сайт", url="https://etodance.com"))
    markup.add(types.InlineKeyboardButton("👥 ЭТО ЛЮДИ", url="https://etodance.com/etofirst"))
    markup.add(types.InlineKeyboardButton("📞 Связаться", url="https://t.me/eto_dance_school"))

    bot.send_message(
        chat_id,
        "Приходи на пробное занятие ЭТО ЛЮДИ! Жми на кнопку в меню.",
        reply_markup=markup
    )

# Отправка видео
def send_video_sequence(chat_id):
    if os.path.exists(video_path):
        with open(video_path, 'rb') as video:
            bot.send_video(chat_id, video)
        time.sleep(5)
    else:
        bot.send_message(chat_id, "Видео пока не загружено. Пожалуйста, добавьте файл video.mp4 в папку проекта.")

# Webhook
@app.route("/", methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@app.route("/")
def index():
    return "Бот работает!"

if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(5)
    bot.set_webhook(url=os.getenv("WEBHOOK_URL"))
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
