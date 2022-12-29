import os
from telegram import InlineKeyboardButton, Chat
from .exceptions import WrongChatID


def form_inline_keyboard(data: dict, num_of_col: int,
                         callback_form: str) -> list:
    """
    Creates an inline keyboard with callback_data in the form of
    provided str + key from provided dictionary.
    """
    keyboard = [[]]
    row = 0
    for i, key in enumerate(data.keys()):
        if i-1 == num_of_col:
            row += 1
            keyboard.append([])
        callback_data = callback_form + key
        keyboard[row].append(InlineKeyboardButton(text=key,
                                                  callback_data=callback_data))
    return keyboard


def check_user(effective_chat: Chat) -> None:
    """Check that the command came from the correct user."""
    chat_id = effective_chat.id
    if chat_id != int(os.getenv('USER_ID')):
        raise WrongChatID(chat_id=chat_id)
