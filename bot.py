from telebot import types
import os
import telebot
from flask import Flask, request
import threading

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

video_path = "video.mp4"

def main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🎥 Смотреть видео")
    bot.send_message(chat_id, 'Первые шаги на пути к свободному танцу от хореографа проекта «Танцы на ТНТ» известного танцовщика Александра Могилёва. Смотри видео!', reply_markup=markup)

@bot.message_handler(commands=["start"])
def handle_start(message):
    main_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text == "🎥 Смотреть видео")
def handle_video(message):
    chat_id = message.chat.id
    send_video_sequence(chat_id)

    # Отложенное сообщение через 120 секунд
    threading.Timer(120, send_followup_links, args=(chat_id,)).start()

def send_video_sequence(chat_id):
    if os.path.exists(video_path):
        with open(video_path, 'rb') as video:
            bot.send_video(chat_id, video)
    else:
        bot.send_message(chat_id, "Видео пока не загружено. Пожалуйста, добавьте файл video.mp4 в папку проекта.")

def send_followup_links(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("👥 ЭТО ЛЮДИ", url="https://etodance.com/etofirst"))
    markup.add(types.InlineKeyboardButton("🌐 Наш сайт", url="https://etodance.com"))
    markup.add(types.InlineKeyboardButton("📞 Связаться", url="https://t.me/eto_dance_school"))
    bot.send_message(chat_id, "Приходи на пробное занятие ЭТО ЛЮДИ! Жми на кнопку в меню.", reply_markup=markup)

@app.route("/", methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@app.route("/")
def index():
    return "Бот работает!"

if __name__ == "__main__":
    bot.remove_webhook()
    threading.Timer(5, lambda: bot.set_webhook(url=os.getenv("WEBHOOK_URL"))).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
