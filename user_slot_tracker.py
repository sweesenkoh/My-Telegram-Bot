from repeated_timer import RepeatedTimer
import slot_database
import telebot

user_tracking_slots = {}

def addUser(timeslot, dateslot, userid):
  global user_tracking_slots
  user_tracking_slots[userid] = [timeslot, dateslot]

def removeUser(userid): 
  global user_tracking_slots
  if (userid in user_tracking_slots):
    del user_tracking_slots[userid]

def __checkUpdateUser():
  global user_tracking_slots
  print(user_tracking_slots)
  usersToRemove = []
  for (key, value) in user_tracking_slots.items():
      if (slot_database.hasAvailableSlot(value[0], value[1])):
        print("Found! notifying user now...")
        telebot.sendMessage(key, f"We found an available slot for ({value[0]} {value[1]}). Go and book now! Quick!! \n\nUse the link here:\nhttps://wis.ntu.edu.sg/webexe88/owa/srce_smain_s.SRC_GenEntry?p_closewind=N")
        usersToRemove.append(key)

  for user in usersToRemove:
    removeUser(user)
  

def startChecking():
  __checkUpdateUser()
  RepeatedTimer(10, __checkUpdateUser)
