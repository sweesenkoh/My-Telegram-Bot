from repeated_timer import RepeatedTimer
import slot_database
import telebot

user_tracking_slots = {}

def addUserSlot(timeslot, dateslot, userid):
  global user_tracking_slots
  if (userid not in user_tracking_slots):
    user_tracking_slots[userid] = [[timeslot, dateslot]]
  else:
    if ([timeslot, dateslot] not in user_tracking_slots[userid]):
      user_tracking_slots[userid].append([timeslot, dateslot])

def removeUserSlot(userid, timeslot, dateslot): 
  global user_tracking_slots
  if (userid in user_tracking_slots):
    if ([timeslot, dateslot] in user_tracking_slots[userid]):
        user_tracking_slots[userid].remove([timeslot, dateslot])
    if (len(user_tracking_slots[userid]) == 0):
      del user_tracking_slots[userid]

def clearUser(userid):
  global user_tracking_slots
  if (userid in user_tracking_slots):
    del user_tracking_slots[userid]

def getTrackingOutputByUserid(userid):
  if (userid not in user_tracking_slots):
    return "You are currently not tracking anything."
  output = ""
  target = user_tracking_slots[userid]
  for (index, slot) in enumerate(target):
    output += f"{index + 1}. {slot[1]} - {slot[0]}\n"
  return output

def __checkUpdateUser():
  global user_tracking_slots
  print(user_tracking_slots)
  usersToRemove = []
  for (key, value) in user_tracking_slots.items():
    for slot in value:
      if (slot_database.hasAvailableSlot(slot[0], slot[1])):
        print("Found! notifying user now...")
        telebot.sendMessage(key, f"We found an available slot for ({slot[0]} {slot[1]}). Go and book now! Quick!! \n\nUse the link here:\nhttps://wis.ntu.edu.sg/webexe88/owa/srce\_smain\_s.SRC\_GenEntry?p\_closewind=N") # need \ to escape _
        usersToRemove.append([key, slot[0], slot[1]])

  for item in usersToRemove:
    removeUserSlot(item[0], item[1], item[2])
  

def startChecking():
  __checkUpdateUser()
  RepeatedTimer(10, __checkUpdateUser)
