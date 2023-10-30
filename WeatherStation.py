from collections import namedtuple
from time import sleep
import numpy as np
import screen_scrolling_testing as SST
import datetime as DT

from file_of_greatness import system_check, days_of_the_week
sense = system_check()

ws = SST.word_scrolling
sleep(1)

ws("power on... testing 1 2 3")

class CurrentTime:
    def __init__(self, time, date, day):
        self.time = time
        self.day = day
        self.date = date
        self._validate()

    def _validate(self):
        if not isinstance(self.time, str) or not isinstance(self.day, str) or not isinstance(self.date, str):
            print("Invaclid time object")
            self.time = "00:00"
            self.day = "Monday"
            self.date = "1970/01/01"

def time_values():
    time_current = str(DT.datetime.now().time().hour) + ":"+ str(DT.datetime.now().time().minute)
    date_current = (str(DT.date.today().year)+ "/"+ str(DT.date.today().month)+ "/"+ str(DT.date.today().day))
    day_current = str(DT.date.today().weekday())
    day_current = days_of_the_week[day_current]
    value = CurrentTime(time_current, date_current, day_current)
    return(value)
temp = sense.get_temperature()


while True:
    event = sense.stick.get_events()
    try: # because this is not always pressed it can and does error when no data input.
        #print(event)
        #print(event[0].direction) # the variable event is a array what holds objects that can be called be calling... 
        if event[0].direction == "up": # ..a point in the array and then the value wanted from the ditionary
            time_value = time_values()
            ws(time_value[0].day)
            sleep(1)
            ws(time_value.date)
            sleep(1)
            ws(time_value.time)
    except Exception as e: # outputs the error message when an error state happens
        print(e)
    sleep(1)
