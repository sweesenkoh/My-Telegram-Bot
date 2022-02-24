import slot_database

def getSlotQueryMessage():
  output = "*Date slots*\n"
  alpha_counter = 97 # a

  for dateslot in slot_database.getSlotDateList():
      output += chr(alpha_counter) + ". " + dateslot + "\n"
      alpha_counter += 1

  output += "\n"
  output += "*Time slots*\n"

  
  for (index, timeslot) in enumerate(slot_database.getTimeSlotsList()):
      output += str(index + 1) + ". " + timeslot + "\n"


  output += "\n\n"
  output += "Please input date slot followed by time slot, for example (a3)"
  
  return output

def processInput(inputChar):
  dateslotChar = inputChar[0]
  timeslotChar = inputChar[1:]
  dateslotIndex = ord(dateslotChar.lower()) - 97
  timeslotIndex = int(timeslotChar) - 1
  return [dateslotIndex, timeslotIndex]