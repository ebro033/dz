#импорт
import requests
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler

# Конфигурация для Telegram бота и API
TOKEN = '6196536692:AAEqynOGy6qdypI8RRf86dtCZx3pkzgebd4'
WEATHER_API_KEY = '2b2ef5eb44f38b2569e1d9beb5bac567'
API_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

# Функция старта бота
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("КИЕВ", callback_data='Kiev'),
         InlineKeyboardButton("Тбилиси", callback_data='Tbilisi')],
        [InlineKeyboardButton("Ввести город вручную", callback_data='input_city')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите город или введите его вручную:', reply_markup=reply_markup)

# Обработчик кнопок для выбора города
def button(update, context):
    query = update.callback_query
    if query.data == "input_city":
        query.message.reply_text("Введите название города, чтобы узнать погоду:")
        return

    get_weather_data(query, query.data)

# Функция для получения и отправки погодных данных указанного города
def get_weather_data(context, city):
    response = requests.get(API_URL.format(city, WEATHER_API_KEY))
    data = response.json()

    if data["cod"] == 200:
        main = data['main']
        weather_info = data['weather'][0]
        msg = f"Погода в {city}:\n\nТемпература: {main['temp'] - 273.15:.2f}°C\nОписание: {weather_info['description']}"
        context.message.reply_text(msg)
    else:
        context.message.reply_text("Не удалось получить погоду для этого города. Попробуйте снова.")

# Обработчик текстовых сообщений
def handle_text(update, context):
    get_weather_data(update, update.message.text)

# Основная функция для запуска бота
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Добавляем обработчики для команд и сообщений
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling()  # Запускаем бота
    updater.idle()  # Ожидаем, пока бот работает

if __name__== '__main__':
    main()