from time import sleep
import numpy as np
import screen_scrolling_testing as SST
import datetime as DT

with open("../info.read", 'r') as info:
    if info.read().__contains__("Xbuntu"):
        from sense_emu import SenseHat
    else:
        from sense_hat import SenseHat
    Sense = SenseHat

ws = SST.word_scrolling
sleep(1)
ws("testing 456")
time_current = str(DT.datetime.now().time())[:5]
date_current = DT.date.today()
#Sense.get_temperature(Sense)