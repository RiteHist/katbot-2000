from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (CallbackContext, ConversationHandler,
                          MessageHandler, filters)
from .utils import form_keyboard, MAIN_BUTTONS, on_back, check_user


BOORU_BUTTONS = ['Select booru',
                 'Get random image',
                 'Add tags',
                 'Select tags',
                 'Search',
                 'Back']

MAIN_MENU, ADD_TAGS, SEARCH = range(3)


async def on_booru(update: Update, context: CallbackContext) -> int:
    check_user(update.effective_chat)
    msg = 'You\'ve selected Booru module. Choose an action.'
    keyboard = ReplyKeyboardMarkup(form_keyboard(BOORU_BUTTONS, 2))
    await update.message.reply_text(text=msg, reply_markup=keyboard)
    return MAIN_MENU


async def get_random_img(update: Update, context: CallbackContext) -> int:
    pass


async def select_booru(update: Update, context: CallbackContext) -> int:
    pass


async def add_tags(update: Update, context: CallbackContext) -> int:
    pass


async def select_tags(update: Update, context: CallbackContext) -> int:
    pass


async def search(update: Update, context: CallbackContext) -> int:
    pass


async def resolve_add_tags(update: Update, context: CallbackContext) -> int:
    pass


async def resolve_search(update: Update, context: CallbackContext) -> int:
    pass

BOORU_CONVERSATION = ConversationHandler(
    entry_points=[MessageHandler(filters.Text(MAIN_BUTTONS[1]), on_booru)],
    states={
        MAIN_MENU: [
            MessageHandler(filters.Text(BOORU_BUTTONS[0]), select_booru),
            MessageHandler(filters.Text(BOORU_BUTTONS[1]), get_random_img),
            MessageHandler(filters.Text(BOORU_BUTTONS[2]), add_tags),
            MessageHandler(filters.Text(BOORU_BUTTONS[3]), select_tags),
            MessageHandler(filters.Text(BOORU_BUTTONS[4]), search)
        ],
        # TODO: Change TEXT to regex
        ADD_TAGS: [MessageHandler(filters.TEXT, resolve_add_tags)],
        SEARCH: [MessageHandler(filters.TEXT, resolve_search)],
    },
    # TODO: Add a fallback for unrecognized text
    fallbacks=[MessageHandler(filters.Text(BOORU_BUTTONS[-1]), on_back)]
)
