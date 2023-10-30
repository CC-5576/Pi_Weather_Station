from time import sleep
import numpy as np
import screen_scrolling_testing as SST
import datetime as DT

with open("info.read", 'r') as info:
    if info.read() == "Xbuntu":
        try:
            from sense_emu import SenseHat #pi os can't install this module so am trying to get it to ignore it
        except:
            pass

    else:
        from sense_hat import SenseHat
    Sense = SenseHat

ws = SST.word_scrolling
sleep(1)
ws("testing 456")
time_current = str(DT.datetime.now().time())[:5]
date_current = DT.date.today()
#Sense.get_temperature(Sense)

date_current = (str(DT.date.today().year)+ ":"+ str(DT.date.today().month)+ ":"+ str(DT.date.today().day))
temp = Sense.get_temperature(Sense())
text = ("Time", time_current, "Date", str(date_current)[:13], "Temp", temp)
print(time_current)
print(date_current)
print(temp)
print(text)
ws(str(text))
