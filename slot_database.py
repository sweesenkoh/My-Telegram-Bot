from repeated_timer import RepeatedTimer
import pandas as pd

GYMSITE_URL = "https://wis.ntu.edu.sg/pls/webexe88/srce_smain_s.srce$sel31_v?choice=1&fcode=NG&fcourt=20&ftype=2"

data = 1

def __updateDatabase():
  print("trying to update data...")
  global data
  df = pd.read_html(GYMSITE_URL)
  slots_df = df[0]
  data = slots_df
  print("updated data...")

def startUpdatingDatabase():
  __updateDatabase()
  RepeatedTimer(30, __updateDatabase)

def getTimeSlotsList():
  return data['Session (hrs)'].unique()

def getSlotDateList():
  return list(filter(lambda column: "202" in column, data.columns))
  
def hasAvailableSlot(timeslot, dateslot):
  try:
    slots = data[data["Session (hrs)"] == timeslot][dateslot].to_list()
    return "Avail" in slots
  except:
    return False
