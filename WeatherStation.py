from keyboard import is_pressed
from collections import namedtuple
from time import sleep
import numpy as np
import screen_scrolling_testing as SST
import datetime as DT

from file_of_greatness import system_check, days_of_the_week
sense = system_check()

ws = SST.word_scrolling

sleep(1)

#ws("power on... testing 1 2 3")

class CurrentTime:
    def __init__(self, time, date, day):
        self.time = time
        self.day = day
        self.date = date
        self._validate()

    def _validate(self):
        if not isinstance(self.time, str) or not isinstance(self.day, str) or not isinstance(self.date, str):
            print("Invalid time object") #i.e. GIVE ME ALL THE DATA
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


class CurrentReadings:
    """returns the current temp, pressure, humidity readings in an object"""
    def __init__(self, current_temp, current_pressure, current_humid):
        self.temperature = current_temp
        self.pressure = current_pressure
        self.humidity = current_humid
        self.validate()
    
    def _validate(self):
        if not isinstance(self.temperature, float) or not isinstance(self.pressure, float) or not isinstance(self.humidity, float):
            print("Invalid sensor data") #i.e. GIVE ME ALL THE DATA (this is just a presense check, suggest change in future 31/10/23 11:40)
            self.temperature = 18
            self.pressure = 1013
            self.humidity = 45


def readings():
    temperature = sense.get_temperature()
    pressure = sense.get_pressure()
    humidity = sense.get_humidity()
    value = CurrentReadings(temperature, pressure, humidity)
    return(value)


while True:
    event = sense.stick.get_events()
    # if is_pressed("C"):
    #     break
    try: # because this is not always pressed it can and does error when no data input.

        print(event[0].direction) # the variable event is a array what holds objects that can be called be calling... 
        if event[0].direction == "up": # ..a point in the array and then the value wanted from the ditionary
            time_value = time_values()
            ws(time_value.day)
            sleep(1)
            ws(time_value.date)
            sleep(1)
            ws(time_value.time)
        
        if event[0].direction == "down":
            sensor_values = readings()
            ws("temperature" + str(sensor_values.temperature))
            sleep(1)
            ws("pressure" + str(sensor_values.pressure))
            sleep(1)
            ws("humidity" + str(sensor_values.humidity))
    except KeyboardInterrupt as e:
        print(e)
        break
    except Exception as e: # outputs the error message when an error state happens
        print(e)
    sleep(1)