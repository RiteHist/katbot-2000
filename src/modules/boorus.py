from os.path import splitext
from urllib.parse import urlparse
import booru
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import (CallbackContext, ConversationHandler,
                          MessageHandler, filters, CallbackQueryHandler)
from .db_util import get_data, put_data
from .exceptions import EmptyBooruResult, NonResolvableResponse
from .utils import form_keyboard, MAIN_BUTTONS, on_back, check_user


BOORU_BUTTONS = ['Select booru',
                 'Get random image',
                 'Add tags',
                 'Select tags',
                 'Delete tags',
                 'Edit tags',
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

MAIN_MENU, ADD_TAGS, SEARCH, DELETE_TAGS, EDIT_TAGS = range(5)


async def on_booru(update: Update, context: CallbackContext) -> int:
    """Initiates booru main menu."""
    check_user(update.effective_chat)
    msg = 'You\'ve selected Booru module. Choose an action.'
    keyboard = ReplyKeyboardMarkup(form_keyboard(BOORU_BUTTONS, 2))
    await update.message.reply_text(text=msg, reply_markup=keyboard)
    return MAIN_MENU


async def get_random_img(update: Update, context: CallbackContext) -> int:
    """
    Gets random image/video/gif from selected booru site
    with selected tags. Tags default to a single whitespace character in case
    that no tags were selected.
    """
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
        search_query = ' '
    try:
        response = await client.search(query=search_query, gacha=True)
    except KeyError:
        raise EmptyBooruResult(booru=selected_client, tags=search_query)
    img_info = booru.resolve(response)
    img_info = resolve_image_response(img_info, selected_tags,
                                      selected_client)
    await resolve_file_extension(img_info, update)
    return MAIN_MENU


def resolve_image_response(image_info: dict, selected_tags: str,
                           selected_client: str) -> tuple[str, str, str]:
    """Gets file path, post url and image extension from booru."""
    keys = ['file_url', '@file_url', 'file']
    image = None
    # Check if any of the keys are in the response
    for key in keys:
        temp = image_info.get(key)
        if key == 'file' and temp:
            temp = temp.get('url')
            if temp:
                image = temp
                break
            else:
                continue
        if temp:
            image = temp
            break
    post_url = image_info.get('post_url', 'Somewhere from paheal')
    if not image:
        raise NonResolvableResponse(selected_client,
                                    selected_tags, image_info)
    img_ext = splitext(urlparse(image).path)[1]
    return (image, post_url, img_ext)


async def resolve_file_extension(image_info: tuple[str, str, str],
                                 update: Update) -> None:
    """
    Sends image/video/animation to user depending on file extension
    with url to original post. If file extension is unknown, sends only
    original post.
    """
    vid_exts = ['.webm', '.avi', '.mp4']
    img_exts = ['.png', '.jpg', '.jpeg', '.bmp', '.svg']
    (image, post_url, image_ext) = image_info
    if image_ext in img_exts:
        await update.message.reply_photo(photo=image,
                                         caption=post_url)
    elif image_ext in vid_exts:
        await update.message.reply_video(video=image,
                                         caption=post_url)
    elif image_ext == '.gif':
        await update.message.reply_animation(animation=image,
                                             caption=post_url)
    else:
        msg = ('Got an unknown file extension.\n'
               f'You can view original post here: {post_url}')
        await update.message.reply_text(msg)


async def select_booru(update: Update, context: CallbackContext) -> int:
    """Gives user an inline keyboard to choose booru client."""
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
    """Gives user an inline keyboard to select tags used for random search."""
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


async def delete_tags(update: Update, context: CallbackContext) -> int:
    return DELETE_TAGS


async def edit_tags(update: Update, context: CallbackContext) -> int:
    return EDIT_TAGS


async def search(update: Update, context: CallbackContext) -> int:
    return SEARCH


async def resolve_add_tags(update: Update, context: CallbackContext) -> int:
    return MAIN_MENU


async def resolve_delete_tags(update: Update, context: CallbackContext) -> int:
    return MAIN_MENU


async def resolve_edit_tags(update: Update, context: CallbackContext) -> int:
    return MAIN_MENU


async def resolve_search(update: Update, context: CallbackContext) -> int:
    return MAIN_MENU


async def btn_select_booru(update: Update, context: CallbackContext) -> int:
    """Changes selected booru after user presses corresponding button."""
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
    """Changes selected tags after user presses corresponding button."""
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


async def btn_delete_tag(update: Update, context: CallbackContext) -> int:
    return DELETE_TAGS


async def btn_edit_tag(update: Update, context: CallbackContext) -> int:
    return EDIT_TAGS


BOORU_CONVERSATION = ConversationHandler(
    entry_points=[MessageHandler(filters.Text(MAIN_BUTTONS[1]), on_booru)],
    states={
        MAIN_MENU: [
            MessageHandler(filters.Text(BOORU_BUTTONS[0]), select_booru),
            MessageHandler(filters.Text(BOORU_BUTTONS[1]), get_random_img),
            MessageHandler(filters.Text(BOORU_BUTTONS[2]), add_tags),
            MessageHandler(filters.Text(BOORU_BUTTONS[3]), select_tags),
            MessageHandler(filters.Text(BOORU_BUTTONS[4]), delete_tags),
            MessageHandler(filters.Text(BOORU_BUTTONS[5]), edit_tags),
            MessageHandler(filters.Text(BOORU_BUTTONS[6]), search),
            CallbackQueryHandler(btn_select_booru, r'setting_booru_\w+', ),
            CallbackQueryHandler(btn_select_tags, r'tag_.+')
        ],
        DELETE_TAGS: [
            CallbackQueryHandler(btn_delete_tag, r'delete_.+'),
            MessageHandler(filters.Regex(r'.+ - .+'), resolve_delete_tags)
        ],
        EDIT_TAGS: [
            CallbackQueryHandler(btn_edit_tag, r'edit_.+'),
            MessageHandler(filters.Regex(r'.+ - .+'), resolve_edit_tags)
        ],
        # TODO: Change TEXT to regex
        ADD_TAGS: [MessageHandler(filters.TEXT, resolve_add_tags)],
        SEARCH: [MessageHandler(filters.TEXT, resolve_search)],
    },
    # TODO: Add a fallback for unrecognized text
    fallbacks=[
        MessageHandler(filters.Text(BOORU_BUTTONS[-1]), on_back),
        MessageHandler(filters.Regex(r'^stop/i$'), on_booru)
    ]
)
