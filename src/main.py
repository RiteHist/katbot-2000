import os
from dotenv import load_dotenv
from telegram.ext import CommandHandler, ApplicationBuilder
import exceptions


load_dotenv()
SECRET_TOKEN = os.getenv('BOT_TOKEN')
USER_ID = int(os.getenv('USER_ID'))


def check_user(effective_chat):
    chat_id = effective_chat.id
    if chat_id != USER_ID:
        raise exceptions.WrongChatID(chat_id=chat_id)


async def error_callback(update, context):
    chat_id = update.effective_chat.id
    if isinstance(context.error, exceptions.WrongChatID):
        msg = 'Sorry, you are not my sweet sweet master.'
        await context.bot.send_message(chat_id=chat_id, text=msg)


async def on_start(update, context):
    chat = update.effective_chat
    check_user(effective_chat=chat)
    name = update.message.chat.first_name
    msg = (f'WHAT IS UP MY RADICAL DUDE!!!!!'
           f'WELCOME TO KATBOT2000 EXPERIENCE, {name}')
    await context.bot.send_message(chat_id=chat.id, text=msg)


def main():
    try:
        application = ApplicationBuilder().token(SECRET_TOKEN).build()
        application.add_error_handler(error_callback)
        application.add_handler(CommandHandler('start', on_start))

        application.run_polling()
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
