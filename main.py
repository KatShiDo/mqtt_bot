from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes, Application, MessageHandler, filters, CommandHandler, CallbackContext, Updater
import os
from charts.charts import *

TOKEN = '6958326278:AAFrhzqsABANo7cKyMSHwGz6UHtJHGopyxI'
BOT_USERNAME = '@MqttMonitorBot'
CHAT_ID = '824304677'
PATH = 'charts'
TIMER = 10
END_JSON = 'data.json'


async def send_images(context: CallbackContext):
    temperature_charts(f'{PATH}/{END_JSON}')
    co2_charts(f'{PATH}/{END_JSON}')

    images = [f for f in os.listdir(PATH) if f.endswith('.png')]
    media_group = [
        InputMediaPhoto(open(f'{PATH}/{images[0]}', 'rb'), caption=f'Статистика значений за последние {TIMER} минут')
    ]

    for image in images[1:]:
        media_group.append(InputMediaPhoto(open(f'{PATH}/{image}', 'rb'), caption=''))

    await context.bot.send_media_group(chat_id=CHAT_ID, media=media_group)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Бот запущен. Используйте команду /help для просмотра списка команд')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Используйте команду /actual для получения последних данных с mqtt')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(f'{PATH}/{END_JSON}', 'r') as file:
        # Load the file contents into a string
        json_string = file.read()

    last_record = json_string.split('{')[-1][:-2]
    temp = last_record.split(',')[0].split(':')[1]
    co2 = last_record.split(',')[1].split(':')[1]
    message = f'Температура: {temp}\nCO2: {co2}'
    await update.message.reply_text(message)

#
# async def send_message(context: CallbackContext):
#     await context.bot.send_message(chat_id=CHAT_ID, text='Hello, world!')


if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('actual', custom_command))

    job_queue = app.job_queue
    job_queue.run_repeating(send_images, interval=TIMER)

    app.run_polling(poll_interval=1)
