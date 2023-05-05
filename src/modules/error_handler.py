from telegram import Update
from telegram.ext import CallbackContext
from .log_conf import logger


async def wrong_id_error(update: Update, **args) -> None:
    msg = 'Sorry, you are not my sweet sweet master.'
    await update.message.reply_text(msg)


async def no_image_url(update: Update, **args) -> None:
    await update.message.reply_text('Something went wrong and'
                                    ' there is no image url.')


async def empty_api_key(update: Update, **args) -> None:
    msg = 'The api key for selected site is empty! Check your .env settings.'
    await update.message.reply_text(msg)


async def empty_site_info(update: Update, **args) -> None:
    msg = 'One of the selected site parameters is empty! Check your logs.'
    await update.message.reply_text(msg)


async def status_code_not_200(update: Update, **args) -> None:
    msg = 'Got an unexpected status code from selected site.'
    await update.message.reply_text(msg)


async def empty_booru_result(update: Update, **args) -> None:
    msg = 'Found nothing with these tags!'
    await update.message.reply_text(msg)


async def non_resolvable_response(update: Update,
                                  context: CallbackContext) -> None:
    response = context.error.response
    post_url = response.get('post_url', 'Somewhere from paheal')
    if post_url:
        msg = ('Got non resolvable response from selected booru. Check logs.'
               f'You can check original post here: {post_url}')
    else:
        msg = 'Got non resolvable response from selected booru. Check logs.'
    await update.message.reply_text(msg)

EXCEPTION_CHOICES = {
    'WrongChatID': wrong_id_error,
    'NoImageURL': no_image_url,
    'EmptyAPIKey': empty_api_key,
    'EmptySiteInfo': empty_site_info,
    'StatusCodeNot200': status_code_not_200,
    'EmptyBooruResult': empty_booru_result,
    'NonResolvableResponse': non_resolvable_response
}


async def error_callback(update: Update, context: CallbackContext) -> None:
    exception_name = context.error.__class__.__name__
    exception_func = EXCEPTION_CHOICES.get(exception_name)
    if exception_func:
        await exception_func(update, context)
    else:
        await update.message.reply_text(str(context.error))
    logger.error(context.error)
    logger.exception('Exception:')
