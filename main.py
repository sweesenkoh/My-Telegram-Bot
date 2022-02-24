from time import sleep
import slot_database
import telebot
import user_slot_tracker


slot_database.startUpdatingDatabase()
sleep(6)
user_slot_tracker.startChecking()
telebot.startTeleBot()


