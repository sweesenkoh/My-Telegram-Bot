from replit_keep_alive import keep_alive
from time import sleep
import slot_database
import telebot
import user_slot_tracker

keep_alive()
slot_database.startUpdatingDatabase()
sleep(6)
user_slot_tracker.startChecking()
telebot.startTeleBot()


