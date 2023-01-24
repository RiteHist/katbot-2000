import os
import requests
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from .db_util import get_data, put_data
from .utils import check_user, form_keyboard
from .exceptions import (NoImageURL, EmptyAPIKey,
                         EmptySiteInfo, StatusCodeNot200)


# TODO: Add a way for user to add new image sources through chat


def get_image_url(target_url: str, image_field: str) -> str:
    """Get image url from target."""
    response = requests.get(target_url)
    if response.status_code != 200:
        raise StatusCodeNot200(response.status_code)
    response = response.json()
    if isinstance(response, dict):
        img = response.get(image_field)
    else:
        img = response[0].get(image_field)
    return img


def post_image(site: str) -> str:
    """Gets site info and constructs a request to it."""
    site_choices = get_data(0, 'funny_sites')
    site_info = site_choices.get(site)
    img_request = site_info.get('request_url')
    img_field = site_info.get('image_field')
    api_param = site_info.get('api_key')
    if api_param:
        api_param = api_param + '='
        api_key = os.getenv(site.upper() + '_API_KEY')
        if not api_key:
            raise EmptyAPIKey(site)
        if '?' in img_request:
            api_param = '&' + api_param
        else:
            api_param = '?' + api_param
        img_request = img_request + api_param + api_key
    if not img_request or not img_field:
        raise EmptySiteInfo(img_request, img_field)
    return get_image_url(img_request, img_field)


async def btn_change_funni(update: Update, context: CallbackContext) -> None:
    """Changes currently selected funny images site."""
    query = update.callback_query
    option = query.data.split('_')[2]
    put_data({'selected_site': option}, 0, 'setting_funny')
    await query.answer(show_alert=False)
    await query.edit_message_text('Select the site for '
                                  'funny images.'
                                  f'\nCurrently selected: {option}',
                                  reply_markup=get_keyboard())


async def on_change_funni(update: Update, context: CallbackContext) -> None:
    """Lets user change the site from which to get funny pictures."""
    check_user(update.effective_chat)
    option = get_data(0, 'setting_funny').get('selected_site')
    if not option:
        option = 'Nothing'
    await update.message.reply_text('Select the site for '
                                    'funny images.'
                                    f'\nCurrently selected: {option}',
                                    reply_markup=get_keyboard())


async def send_funny_image(update: Update, context: CallbackContext) -> None:
    """Sends an image from selected source site."""
    check_user(update.effective_chat)
    curr_site = get_data(0, 'setting_funny').get('selected_site')
    if not curr_site:
        await update.message.reply_text('You must select the site with funny'
                                        'images with /change_funni command')
    image = post_image(curr_site)
    if not image:
        raise NoImageURL(image)
    if image.endswith('.gif'):
        await update.message.reply_animation(image)
    else:
        await update.message.reply_photo(image)


def get_keyboard() -> InlineKeyboardMarkup:
    """Forms an inline keyboard from funny sites selection."""
    site_choices = get_data(0, 'funny_sites')
    keyboard = form_keyboard(data=site_choices.keys(),
                             num_of_col=2, inline=True,
                             callback_form='setting_funny_')
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup
