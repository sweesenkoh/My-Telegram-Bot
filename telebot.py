import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram 
import input_processor
import slot_database
import user_slot_tracker
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


TELEBOT_API_TOKEN = "SECRET"

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def __start(update, context):
    """Send a message when the command /start is issued."""
    bot = telegram.Bot(token=TELEBOT_API_TOKEN)
    userid = update.message.chat.id
    bot.send_message(chat_id=userid, text=input_processor.getSlotQueryMessage(), parse_mode= 'Markdown')


def __help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')
  


def __echo(update, context):
    """Echo the user message."""
    try:
      result = input_processor.processInput(update.message.text)
      dateindex = result[0]
      timeslotIndex = result[1]

      selectedDate = slot_database.getSlotDateList()[dateindex]
      selectedTime = slot_database.getTimeSlotsList()[timeslotIndex]

      user_slot_tracker.addUser(selectedTime, selectedDate, update.message.chat.id)
      update.message.reply_text(f"Successfully added your tracking request for ({selectedDate} {selectedTime})")
    except Exception as e:
      update.message.reply_text("Sorry I cannot interprete what you just told me, can you please read the instruction and input properly? If you don't know what to do, please input /start command first, thanks.")


def __error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def sendMessage(userid, text):
    bot = telegram.Bot(token=TELEBOT_API_TOKEN)
    bot.send_message(chat_id=userid, text=text, parse_mode= 'Markdown')

def startTeleBot():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TELEBOT_API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", __start))
    dp.add_handler(CommandHandler("help", __help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, __echo))

    # log all errors
    dp.add_error_handler(__error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
