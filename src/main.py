import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler


load_dotenv()
SECRET_TOKEN = os.getenv('BOT_TOKEN')


def on_start(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    msg = (f'WHAT IS UP MY RADICAL DUDE!!!!!'
           f'WELCOME TO KATBOT2000 EXPERIENCE, {name}')
    context.bot.send_message(chat_id=chat.id, text=msg)


def main():
    try:
        updater = Updater(token=SECRET_TOKEN)
        updater.dispatcher.add_handler(CommandHandler('start', on_start))

        updater.start_polling()
        updater.idle()
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
