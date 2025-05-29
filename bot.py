import os
import telebot
from telebot import types
import time
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🎥 Смотреть видео")
    keyboard.row("📞 Связаться с нами", "🌐 Наш сайт")
    keyboard.row("👥 ЭТО ЛЮДИ")
    return keyboard

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Привет! Готов начать путь? Жми кнопку ниже 👇",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    if message.text == "🎥 Смотреть видео":
        send_video_sequence(message.chat.id)
    elif message.text == "📞 Связаться с нами":
        bot.send_message(message.chat.id, "Связь: @your_contact_username")
    elif message.text == "🌐 Наш сайт":
        bot.send_message(message.chat.id, "Вот наш сайт: https://yourwebsite.com")
    elif message.text == "👥 ЭТО ЛЮДИ":
        bot.send_message(message.chat.id, "Это настоящие люди, вот их отзывы: https://yourreviews.com")

def send_video_sequence(chat_id):
    video_path = "static/video.mp4"
    if os.path.exists(video_path):
        with open(video_path, 'rb') as video:
            bot.send_video(chat_id, video)
        time.sleep(30)
        bot.send_message(chat_id, "Хочешь получить пробный урок? Напиши нам прямо сейчас!")
    else:
        bot.send_message(chat_id, "Видео пока не загружено. Пожалуйста, добавьте файл video.mp4 в папку static.")

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@app.route('/')
def index():
    return "Бот работает!"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{os.getenv('WEBHOOK_URL')}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
