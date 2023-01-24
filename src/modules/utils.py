import os
from telegram import (InlineKeyboardButton, Chat,
                      Update, ReplyKeyboardMarkup)
from telegram.ext import CallbackContext, ConversationHandler
from .exceptions import WrongChatID


MAIN_BUTTONS = ['Get funny image',
                'Boorus',
                'Organizer',
                'Torrents']


def form_keyboard(data: list, num_of_col: int,
                  inline=False, callback_form='') -> list:
    """
    Forms a balanced keyboard from provided list of strings.
    If inline argument is set to True, will form an inline keyboard
    with a button text taken from data argument and callback_data as a
    concatenation of callback_form argument and button text.
    """
    keyboard = [[]]
    row = 0
    for i, text in enumerate(data):
        if i % num_of_col == 0:
            row += 1
            keyboard.append([])
        if inline:
            callback_data = callback_form + text
            (keyboard[row]
             .append(InlineKeyboardButton(text=text,
                                          callback_data=callback_data)))
        else:
            keyboard[row].append(text)

    return keyboard


def check_user(effective_chat: Chat) -> None:
    """Check that the command came from the correct user."""
    chat_id = effective_chat.id
    if chat_id != int(os.getenv('USER_ID')):
        raise WrongChatID(chat_id=chat_id)


async def on_back(update: Update, context: CallbackContext) -> int:
    """Gives user main menu keyboard."""
    keyboard = ReplyKeyboardMarkup(form_keyboard(MAIN_BUTTONS, 2))
    msg = 'What would you like to do?'
    await update.message.reply_text(text=msg,
                                    reply_markup=keyboard)
    return ConversationHandler.END
