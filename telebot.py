import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram 
import input_processor
import slot_database
import user_slot_tracker
from session_state_enum import SessionState

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

user_session = {}

def removeUserFromSession(userid):
  if (userid) in user_session:
    del user_session[userid]

TELEBOT_API_TOKEN = "SECRET"

def __start(update, context):
    bot = telegram.Bot(token=TELEBOT_API_TOKEN)
    userid = update.message.chat.id
    removeUserFromSession(userid)
    bot.send_message(chat_id=userid, text=getGenericWelcomeMessage(), parse_mode= 'Markdown')

def __add(update, context):
    bot = telegram.Bot(token=TELEBOT_API_TOKEN)
    userid = update.message.chat.id
    user_session[userid] = SessionState.ADD
    bot.send_message(chat_id=userid, text=input_processor.getSlotQueryMessage(), parse_mode= 'Markdown')

def __check(update, context):
  bot = telegram.Bot(token=TELEBOT_API_TOKEN)
  userid = update.message.chat.id
  user_session[userid] = SessionState.CHECK
  bot.send_message(chat_id=userid, text=input_processor.getSlotQueryMessage(), parse_mode= 'Markdown')

def __tracking(update, context):
    userid = update.message.chat.id
    removeUserFromSession(userid)
    output = user_slot_tracker.getTrackingOutputByUserid(userid)
    update.message.reply_text(output)

def __clear(update, context):
    userid = update.message.chat.id
    removeUserFromSession(userid)
    user_slot_tracker.clearUser(userid)
    update.message.reply_text("Removed!")

def __remove(update, context):
  userid = update.message.chat.id
  output = user_slot_tracker.getTrackingOutputByUserid(userid)
  if ("not tracking anything" in output): # clearly not supposed to write this way but too lazy
    update.message.reply_text(output)
    return
  user_session[userid] = SessionState.REMOVE
  update.message.reply_text(f"Please input the slot number that you want to remove: \n\n{output}")

def __echo(update, context):
    """Echo the user message."""
    userid = update.message.chat.id
    if (userid not in user_session):
      update.message.reply_text(getGenericWelcomeMessage(), parse_mode= 'Markdown')
      return

    if (user_session[userid] == SessionState.ADD or user_session[userid] == SessionState.CHECK):
      temp = user_session[userid]
      removeUserFromSession(userid)
      try:
        result = input_processor.processInput(update.message.text)
        dateindex = result[0]
        timeslotIndex = result[1]
  
        selectedDate = slot_database.getSlotDateList()[dateindex]
        selectedTime = slot_database.getTimeSlotsList()[timeslotIndex]
        if (temp == SessionState.ADD):
          user_slot_tracker.addUserSlot(selectedTime, selectedDate, update.message.chat.id)
          update.message.reply_text(f"Successfully added your tracking request for ({selectedDate} {selectedTime})")
        elif (temp == SessionState.CHECK):
          slotAvailable = slot_database.hasAvailableSlot(selectedTime, selectedDate)
          
          update.message.reply_text(f"There is currently {slot_database.checkNumberOfAvailableSlot(selectedTime, selectedDate)} slots available" if slotAvailable else "There are no slots available")
        return
      except Exception as e:
        update.message.reply_text("Sorry I cannot interprete what you just told me, can you please read the instruction and input properly? If you don't know what to do, please input /start command first, thanks.")
        return

    if (user_session[userid] == SessionState.REMOVE):
      removeUserFromSession(userid)
      try:
        target = user_slot_tracker.user_tracking_slots[userid]
        userInput = int(update.message.text) - 1
        if (userInput < 0 or userInput >= len(target)):
          raise Exception("Something wrong")

        temp = target[userInput]
        del target[userInput]
        update.message.reply_text(f"Removed: {temp[0]} {temp[1]}")
        # delete the specific slot that is specified by the user_session
        # output = user_slot_tracker.getTrackingOutputByUserid(userid)
        return
      except:
        update.message.reply_text(f"You did something wrong.")
        return

    # base case just return welcome message, should not reach here by right
    update.message.reply_text(getGenericWelcomeMessage(), parse_mode= 'Markdown')

def __error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def sendMessage(userid, text):
    bot = telegram.Bot(token=TELEBOT_API_TOKEN)
    bot.send_message(chat_id=userid, text=text, parse_mode= 'Markdown')

def getGenericWelcomeMessage():
  return """*Use the following commands to get started*:
  /add - Add new slot to be tracked
  /tracking - See all the slots that you are currently tracking
  /remove - Remove a slot from tracking list
  /clear - Clear all items from the tracking list
  /check - Check whether a slot is currently available for booking
  """

def startTeleBot():
    updater = Updater(TELEBOT_API_TOKEN, use_context=True)
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", __start))
    dp.add_handler(CommandHandler("add", __add))
    dp.add_handler(CommandHandler("tracking", __tracking))
    dp.add_handler(CommandHandler("remove", __remove))
    dp.add_handler(CommandHandler("clear", __clear))
    dp.add_handler(CommandHandler("check", __check))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, __echo))

    # log all errors
    dp.add_error_handler(__error)

    # Start the Bot
    updater.start_polling()
    updater.idle()
