from telegram import Update
from telegram.ext import CallbackContext
from .exceptions import (WrongChatID, NoImageURL,
                         EmptyAPIKey, EmptySiteInfo,
                         StatusCodeNot200)
from .log_conf import logger


async def wrong_id_error(update: Update) -> None:
    msg = 'Sorry, you are not my sweet sweet master.'
    await update.message.reply_text(msg)


async def no_image_url(update: Update) -> None:
    await update.message.reply_text('Something went wrong and'
                                    ' there is no image url.')


async def empty_api_key(update: Update) -> None:
    msg = 'The api key for selected site is empty! Check your .env settings.'
    await update.message.reply_text(msg)


async def empty_site_info(update: Update) -> None:
    msg = 'One of the selected site parameters is empty! Check your logs.'
    await update.message.reply_text(msg)


async def status_code_not_200(update: Update) -> None:
    msg = 'Got an unexpected status code from selected site.'
    await update.message.reply_text(msg)


async def error_callback(update: Update, context: CallbackContext) -> None:
    if isinstance(context.error, WrongChatID):
        await wrong_id_error(update)
    if isinstance(context.error, NoImageURL):
        await no_image_url(update)
    if isinstance(context.error, EmptyAPIKey):
        await empty_api_key(update)
    if isinstance(context.error, EmptySiteInfo):
        await empty_site_info(update)
    if isinstance(context.error, StatusCodeNot200):
        await status_code_not_200(update)
    logger.exception('Got the following exception:')
