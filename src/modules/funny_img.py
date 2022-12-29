import requests
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from .db_util import get_data, put_data
from .utils import form_inline_keyboard, check_user


def get_image_url(target_url: str) -> str:
    """Get image url from target."""
    response = requests.get(target_url)
    response = response.json()
    return response[0].get('url')


def post_image(site: str) -> str:
    site_choices = get_data(0, 'funny_sites')
    img_url = site_choices.get(site)
    if not img_url:
        return None
    return get_image_url(img_url)


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
    check_user(update.effective_chat)
    curr_site = get_data(0, 'setting_funny').get('selected_site')
    if not curr_site:
        await update.message.reply_text('You must select the site with funny'
                                        'images with /change_funni command')
    image = post_image(curr_site)
    if not image:  # TODO add an exception throw
        await update.message.reply_text('Something went wrong and'
                                        ' there is no image url.')
    await update.message.reply_photo(image)


def get_keyboard() -> InlineKeyboardMarkup:
    site_choices = get_data(0, 'funny_sites')
    keyboard = form_inline_keyboard(site_choices, 2, 'setting_funny_')
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup
