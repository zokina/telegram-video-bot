
import os
import telebot
from flask import Flask, request
import time

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

video_path = "video.mp4"

def main_menu(chat_id):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🎥 Смотреть видео")
    markup.row("📞 Связаться с нами", "🌐 Наш сайт", "👥 ЭТО ЛЮДИ")
    bot.send_message(chat_id, "Первые шаги на пути к свободному танцу от директора школы ЭТО Александра Могилева. Жми на кнопку "Смотреть видео"", reply_markup=markup)

@bot.message_handler(commands=["start"])
def handle_start(message):
    main_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text == "🎥 Смотреть видео")
def handle_video(message):
    chat_id = message.chat.id
    send_video_sequence(chat_id)

@bot.message_handler(func=lambda message: message.text == "📞 Связаться с нами")
def handle_contact(message):
    bot.send_message(message.chat.id, "Связь: @eto_dance_school")

@bot.message_handler(func=lambda message: message.text == "🌐 Наш сайт")
def handle_website(message):
    bot.send_message(message.chat.id, "Вот наш сайт: https://etodance.com")

@bot.message_handler(func=lambda message: message.text == "👥 ЭТО ЛЮДИ")
def handle_people(message):
    bot.send_message(message.chat.id, "Начни танцевать: https://etodance.com/people")

def send_video_sequence(chat_id):
    if os.path.exists(video_path):
        with open(video_path, 'rb') as video:
            bot.send_video(chat_id, video)
        time.sleep(5)
        bot.send_message(chat_id, "Если хочешь задать вопрос — напиши нам!")
    else:
        bot.send_message(chat_id, "Видео пока не загружено. Пожалуйста, добавьте файл video.mp4 в папку проекта.")

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
