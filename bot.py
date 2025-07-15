from telebot import types
import os
import telebot
from flask import Flask, request
import time
import threading
import datetime

# Токен бота
TOKEN = "8193200259:AAFanSNesmdce0ISr6CtHgOiwrmay6SgPVw"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

video_path = "video.mp4"

def main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🎥 Смотреть видео")
    bot.send_message(
        chat_id,
        "Ваши первые шаги на пути к новой жизни, без страхов, стеснения, эмоционального и физического напряжения, благодаря свободному танцу от хореографа проекта «Танцы на ТНТ» известного танцовщика Александра Могилёва. Смотрите видео ⬇",
        reply_markup=markup
    )

@bot.message_handler(commands=["start"])
def handle_start(message):
    main_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text == "🎥 Смотреть видео")
def handle_video(message):
    chat_id = message.chat.id
    send_video_sequence(chat_id)
    threading.Timer(120, send_followup_links, args=(chat_id,)).start()
    schedule_notifications(chat_id)  # Добавляем планирование уведомлений

def send_video_sequence(chat_id):
    if os.path.exists(video_path):
        with open(video_path, 'rb') as video:
            bot.send_video(
                chat_id,
                video,
                supports_streaming=True,
                width=720,
                height=1280,
                duration=183
            )
    else:
        bot.send_message(chat_id, "Видео пока не загружено. Пожалуйста, добавьте файл video.mp4 в папку проекта.")

def send_followup_links(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("👥 Это люди - оплатить за 499 руб", url="https://etodance.com/payment"))
    markup.add(types.InlineKeyboardButton("🌐 Наш сайт", url="https://etodance.com/etofirst"))
    markup.add(types.InlineKeyboardButton("📞 Узнать подробности", url="https://t.me/eto_dance_school"))
    markup.add(types.InlineKeyboardButton("❤️ Другие направления школы", url="https://etodance.com/"))
    bot.send_message(chat_id, "Мы поможем Вам раскрыться! Танец — это Ваш способ вернуть энергию, избавиться от стресса и стать уверенней в себе. Приходите на пробное занятие «ЭТО ЛЮДИ» всего за 999 и начните двигаться свободно в дружелюбной и непринуждённой атмосфере. Жмите кнопку — сделайте первый шаг к новой жизни уже сегодня!", reply_markup=markup)

# 📹 Обработчик видео, отправленного как видео
@bot.message_handler(content_types=['video'])
def get_video_id(message):
    if message.video:
        bot.send_message(
            message.chat.id,
            f"file_id (video): `{message.video.file_id}`",
            parse_mode='Markdown'
        )

# 📎 Обработчик видео, отправленного как файл-документ
@bot.message_handler(content_types=['document'])
def get_video_as_document(message):
    if message.document.mime_type and message.document.mime_type.startswith("video"):
        bot.send_message(
            message.chat.id,
            f"file_id (document): `{message.document.file_id}`",
            parse_mode='Markdown'
        )

# Добавляем таймеры для уведомлений
def schedule_notifications(chat_id):
    # Уведомление через неделю
    one_week_later = datetime.datetime.now() + datetime.timedelta(weeks=1)
    threading.Timer((one_week_later - datetime.datetime.now()).total_seconds(), send_weekly_notification, args=(chat_id,)).start()

    # Уведомление через две недели
    two_weeks_later = datetime.datetime.now() + datetime.timedelta(weeks=2)
    threading.Timer((two_weeks_later - datetime.datetime.now()).total_seconds(), send_two_week_notification, args=(chat_id,)).start()

    # Уведомление через месяц
    one_month_later = datetime.datetime.now() + datetime.timedelta(weeks=4)
    threading.Timer((one_month_later - datetime.datetime.now()).total_seconds(), send_monthly_notification, args=(chat_id,)).start()

def send_weekly_notification(chat_id):
    bot.send_message(
        chat_id,
        "Мечтаете избавиться от стресса и тревоги? Танец поможет Вам расслабиться и почувствовать себя лучше. Без конкуренции, критики и стеснения. С поддержкой сильнейших педагогов страны! Запишитесь на пробное занятие всего за 499 рублей."
    )

def send_two_week_notification(chat_id):
    bot.send_message(
        chat_id,
        "Страдаете от нехватки энергии и мотивации? Проведите время в дружелюбной атмосфере школы танцев А.Могилева без конкуренции и осуждения. Пусть движение станет Вашим источником силы — бронируйте пробное за 499 рублей и начните менять жизнь в лучшую сторону. Количество мест ограничено!"
    )

def send_monthly_notification(chat_id):
    bot.send_message(
        chat_id,
        "Сделайте первый шаг к лучшей жизни! С помощью танца и сильнейших педагогов страны, Вы легко и просто зарядитесь энергией и позитивом, избавитесь от скованности и зажатости. Вы увидите результат и почувствуете уверенность в себе уже после 1 занятия. Запишитесь на пробное за 499 рублей и почувствуйте, как оживает Ваше тело и душа."
    )

@app.route("/", methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@app.route("/")
def index():
    return "Бот работает!"

if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(1)
    # Используем твой WEBHOOK_URL
    bot.set_webhook(url="https://telegram-video-bot-1lek.onrender.com")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    # фиктивное изменение для перезапуска
