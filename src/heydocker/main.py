import json
import logging
import os
import re
import subprocess
from functools import wraps

from telegram import ForceReply, Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters)

from heydocker import AUDIO, PHOTO, PHOTO_URL, TEXT, VIDEO
from heydocker.functions import run

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

token = os.environ.get("TELEGRAM_TOKEN")

if token is None:
    raise ValueError("TELEGRAM_TOKEN environment variable not set.")

allowed_ids = os.environ.get("ALLOWED_IDS")
logger.info(f"Allow IDs: {allowed_ids}")
if allowed_ids:
    allowed_ids = [int(x) for x in allowed_ids.split(",")]
else:
    allowed_ids = []

logger.info(f"Allow IDs: {allowed_ids}")


def check_user_allowed(command_handler):
    @wraps(command_handler)
    async def wrapper(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        id = update.effective_user.id
        if id in allowed_ids:
            return await command_handler(update, context, *args, **kwargs)
        else:
            await update.message.reply_text(
                "You are not authorized to use this command."
            )

    return wrapper


# Define a few command handlers. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


@check_user_allowed
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


@check_user_allowed
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the user message."""
    logger.info(f"User question: {update.message.text}")
    if update.message.text == "Restart the container dockerbot for me":
        await update.message.reply_text("Fuck you")
    else:
        response = run(update.message.text)
        logger.info(f"Response message: {response}")

        await update.message.reply_text(response)


def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
