import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ApplicationBuilder, MessageHandler
from telegram.ext import CallbackContext, filters, CallbackQueryHandler
from modules.boorus import BOORU_CONVERSATION
from modules.funny_img import (send_funny_image,
                               on_change_funni,
                               btn_change_funni)
from modules.utils import check_user, form_keyboard, on_back
from modules.log_conf import logger
from modules.error_handler import error_callback
from modules.utils import MAIN_BUTTONS


load_dotenv()
SECRET_TOKEN = os.getenv('BOT_TOKEN')


async def on_start(update: Update, context: CallbackContext) -> None:
    """Starts the bot with a greeting message and a button keyboard."""
    chat = update.effective_chat
    check_user(effective_chat=chat)
    keyboard_buttons = form_keyboard(MAIN_BUTTONS, 2)
    keyboard = ReplyKeyboardMarkup(keyboard_buttons)
    bot_info = await context.bot.get_me()
    bot_name = bot_info.first_name.upper()
    name = update.message.chat.first_name.upper()
    msg = (f'WHAT IS UP MY RADICAL DUDE!!!!!'
           f'WELCOME TO {bot_name} EXPERIENCE, {name}!')
    await context.bot.send_message(chat_id=chat.id, text=msg)
    msg = 'What would you like to do?'
    await update.message.reply_text(text=msg,
                                    reply_markup=keyboard)
    logger.info(f'Started a new chat with id {chat.id}')


def main() -> None:
    try:
        application = ApplicationBuilder().token(SECRET_TOKEN).build()
        application.add_error_handler(error_callback)
        application.add_handler(CommandHandler('start', on_start))
        application.add_handler(CommandHandler('change_funni',
                                               on_change_funni))
        application.add_handler(MessageHandler(filters.Text(MAIN_BUTTONS[0]),
                                               send_funny_image))
        application.add_handler(CallbackQueryHandler(btn_change_funni,
                                                     r'setting_funny_\w+'))
        application.add_handler(BOORU_CONVERSATION)
        application.add_handler(MessageHandler(filters.Text('Back'), on_back))

        application.run_polling()
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
