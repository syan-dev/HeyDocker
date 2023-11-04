import os
import re
import logging
import subprocess
import docker
from functools import wraps
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

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
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        id = update.effective_user.id
        if id in allowed_ids:
            return await command_handler(update, context, *args, **kwargs)
        else:
            await update.message.reply_text("You are not authorized to use this command.")
    
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
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


@check_user_allowed
async def check_ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check machine memory."""
    ip_address = subprocess.check_output(['curl','ipinfo.io/ip']).decode('utf-8')
    await update.message.reply_text(ip_address)


@check_user_allowed
async def check_net(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check machine network."""
    try:
        x = subprocess.check_output(['speedtest-cli','--share']).decode('utf-8')
    except subprocess.CalledProcessError as e:
        await update.message.reply_text("Network speed test failed.")
        return
    
    photo_match = re.search("(?P<url>https?://[^\s]+)", x)
    if photo_match:
        photo_url = photo_match.group("url")
        await update.message.reply_photo(photo_url)
    else:
        await update.message.reply_text("Network speed test result not found.")


@check_user_allowed
async def list_docker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List docker containers."""
    client = client = docker.from_env()
    containers = client.containers.list(all=True)
    message = ""
    for container in containers:
        message += f"{container.name} - {container.status}\n"
    
    await update.message.reply_text(message)


@check_user_allowed
async def run_docker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Run docker container."""
    client = client = docker.from_env()
    logger.info('Running docker container')
    message = client.containers.run("ubuntu:latest", "echo hello world").decode('utf-8')
    logger.info(message)
    
    await update.message.reply_text('Run Docker ubuntu:latest successful, echo'+message)


def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()
    
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ip", check_ip))
    application.add_handler(CommandHandler("net", check_net))
    application.add_handler(CommandHandler("list", list_docker))
    application.add_handler(CommandHandler("run", run_docker))
    # application.add_handler(CommandHandler("mem", check_memory))
    # application.add_handler(CommandHandler("cpu", check_cpu))
    # application.add_handler(CommandHandler("disk", check_disk))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)