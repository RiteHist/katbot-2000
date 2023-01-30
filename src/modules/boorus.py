import booru
from random import randint
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import (CallbackContext, ConversationHandler,
                          MessageHandler, filters, CallbackQueryHandler)
from .db_util import get_data, put_data
from .utils import form_keyboard, MAIN_BUTTONS, on_back, check_user


BOORU_BUTTONS = ['Select booru',
                 'Get random image',
                 'Add tags',
                 'Select tags',
                 'Search',
                 'Back']

BOORU_CLIENTS = {
    'ATFbooru': booru.Atfbooru,
    'Behoimi': booru.Behoimi,
    'Danbooru': booru.Danbooru,
    'Derpibooru': booru.Derpibooru,
    'E621': booru.E621,
    'E926': booru.E926,
    'Furbooru': booru.Furbooru,
    'Gelbooru': booru.Gelbooru,
    'Hypnohub': booru.Hypnohub,
    'Konachan': booru.Konachan,
    'Konachan.net': booru.Konachan_Net,
    'Lolibooru': booru.Lolibooru,
    'Paheal': booru.Paheal,
    'Realbooru': booru.Realbooru,
    'Rule34': booru.Rule34,
    'Safebooru': booru.Safebooru,
    'Tbib': booru.Tbib,
    'Xbooru': booru.Xbooru,
    'Yandere': booru.Yandere
}

MAIN_MENU, ADD_TAGS, SEARCH = range(3)


async def on_booru(update: Update, context: CallbackContext) -> int:
    check_user(update.effective_chat)
    msg = 'You\'ve selected Booru module. Choose an action.'
    keyboard = ReplyKeyboardMarkup(form_keyboard(BOORU_BUTTONS, 2))
    await update.message.reply_text(text=msg, reply_markup=keyboard)
    return MAIN_MENU


async def get_random_img(update: Update, context: CallbackContext) -> int:
    selected_client = get_data(0, 'setting_booru').get('selected_client')
    if not selected_client:
        msg = 'Please select the booru first!'
        await update.message.reply_text(text=msg)
        return MAIN_MENU
    client = BOORU_CLIENTS.get(selected_client)()
    selected_tags = get_data(0, 'setting_tags').get('selected_tags')
    if selected_tags:
        search_query = get_data(0, 'booru_tags').get(selected_tags)
    else:
        search_query = 'order:random'
    response = await client.search_image(query=search_query)
    images = booru.resolve(response)
    r_num = randint(0, len(images) - 1)
    image = images[r_num]
    if not image:
        msg = 'Something went wrong'
        await update.message.reply_text(text=msg)
        return MAIN_MENU
    await update.message.reply_photo(image)
    return MAIN_MENU


async def select_booru(update: Update, context: CallbackContext) -> int:
    selected = get_data(0, 'setting_booru').get('selected_client')
    if not selected:
        selected = 'Nothing'
    msg = f'Select a booru client to use. Currently selected: {selected}.'
    reply_markup = InlineKeyboardMarkup(
        form_keyboard(data=BOORU_CLIENTS.keys(), num_of_col=2,
                      inline=True, callback_form='setting_booru_')
    )
    await update.message.reply_text(text=msg, reply_markup=reply_markup)
    return MAIN_MENU


async def add_tags(update: Update, context: CallbackContext) -> int:
    return ADD_TAGS


async def select_tags(update: Update, context: CallbackContext) -> int:
    tags = get_data(0, 'booru_tags')
    if not tags:
        await update.message.reply_text(
            text='No saved tags found! Please add some tags to select them!'
        )
        return MAIN_MENU
    selected = get_data(0, 'setting_tags').get('selected_tags')
    if not selected:
        selected = 'Nothing'
    msg = ('Select a group of tags to use for your next random search. '
           f'Currently you\'ve selected {selected}.')
    reply_markup = InlineKeyboardMarkup(
        form_keyboard(data=tags.keys(), num_of_col=1,
                      inline=True, callback_form='tag_')
    )
    await update.message.reply_text(text=msg, reply_markup=reply_markup)
    return MAIN_MENU


async def search(update: Update, context: CallbackContext) -> int:
    return SEARCH


async def resolve_add_tags(update: Update, context: CallbackContext) -> int:
    return MAIN_MENU


async def resolve_search(update: Update, context: CallbackContext) -> int:
    return MAIN_MENU


async def btn_select_booru(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    selected = query.data.split('_')[2]
    put_data({'selected_client': selected}, 0, 'setting_booru')
    await query.answer(show_alert=False)
    msg = f'You\'ve selected: {selected}.'
    reply_markup = InlineKeyboardMarkup(
        form_keyboard(data=BOORU_CLIENTS.keys(), num_of_col=2,
                      inline=True, callback_form='setting_booru_')
    )
    await query.edit_message_text(text=msg, reply_markup=reply_markup)
    return MAIN_MENU


async def btn_select_tags(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    selected = query.data.split('_')[1]
    put_data({'selected_tags': selected}, 0, 'setting_tags')
    tags = get_data(0, 'booru_tags')
    tags_in_group = tags.get(selected)
    await query.answer(show_alert=False)
    msg = (f'You\'ve selected the group {selected}.\n'
           'Here are the tags in that group:\n'
           f'{tags_in_group}')
    reply_markup = InlineKeyboardMarkup(
        form_keyboard(data=tags.keys(), num_of_col=1,
                      inline=True, callback_form='tag_')
    )
    await query.edit_message_text(text=msg, reply_markup=reply_markup)
    return MAIN_MENU

BOORU_CONVERSATION = ConversationHandler(
    entry_points=[MessageHandler(filters.Text(MAIN_BUTTONS[1]), on_booru)],
    states={
        MAIN_MENU: [
            MessageHandler(filters.Text(BOORU_BUTTONS[0]), select_booru),
            MessageHandler(filters.Text(BOORU_BUTTONS[1]), get_random_img),
            MessageHandler(filters.Text(BOORU_BUTTONS[2]), add_tags),
            MessageHandler(filters.Text(BOORU_BUTTONS[3]), select_tags),
            MessageHandler(filters.Text(BOORU_BUTTONS[4]), search),
            CallbackQueryHandler(btn_select_booru, r'setting_booru_\w+', ),
            CallbackQueryHandler(btn_select_tags, r'tag_.+')
        ],
        # TODO: Change TEXT to regex
        ADD_TAGS: [MessageHandler(filters.TEXT, resolve_add_tags)],
        SEARCH: [MessageHandler(filters.TEXT, resolve_search)],
    },
    # TODO: Add a fallback for unrecognized text
    fallbacks=[MessageHandler(filters.Text(BOORU_BUTTONS[-1]), on_back)]
)
