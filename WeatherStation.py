from time import sleep
import numpy as np
import screen_scrolling_testing as SST
import datetime as DT

from file_of_greatness import system_check
sense = system_check()

ws = SST.word_scrolling
sleep(1)
ws("testing 456")
"""
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
"""