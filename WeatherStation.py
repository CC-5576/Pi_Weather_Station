#from keyboard import is_pressed
#from collections import namedtuple
import logging
from time import sleep
import numpy as np
import screen_scrolling_testing as SST
import datetime as DT
try:
    from gpiozero import CPUTemperature; CPU_temp = CPUTemperature().temperature
except:
    CPU_temp = 60
from file_of_greatness import system_check, days_of_the_week

with open("iteration_count", "r") as current_iteration:
    current_iteration = int(current_iteration.read())
    with open("iteration_count", "w") as new_iteration:
        new_iteration.write(str(current_iteration+1))
        new_iteration.close()

sense = system_check()

ws = SST.word_scrolling

filename = str(DT.date.today())+"_"+str(current_iteration+1)+"sensor_output.txt" #creates a new unique file name for every new run

iteration_count = 0

event_count = 0
sleep(1)

#ws("power on... testing 1 2 3")

class CurrentTime:
    def __init__(self, time, date, day, full_time):
        self.time = time
        self.day = day
        self.date = date
        self.full_time = full_time
        self.error = "Passed"
        self._validate()

    def _validate(self):
        if not isinstance(self.time, str) or not isinstance(self.day, str) or not isinstance(self.date, str):
            print("Invalid time object") #i.e. GIVE ME ALL THE DATA
            self.time = "00:00"
            self.day = "Monday"
            self.date = "1970/01/01"
            self.error = "Invalid time object"

def time_values():
    time_current = str(DT.datetime.now().time().hour) + ":"+ str(DT.datetime.now().time().minute)
    date_current = (str(DT.date.today().year)+ "/"+ str(DT.date.today().month)+ "/"+ str(DT.date.today().day))
    day_current = str(DT.date.today().weekday())
    full_time = str(DT.datetime.now())
    day_current = days_of_the_week[day_current]
    value = CurrentTime(time_current, date_current, day_current, full_time)
    return(value)


class CurrentReadings:
    """returns the current temp, pressure, humidity readings in an object"""
    def __init__(self, current_temp, current_pressure, current_humid):
        self.temperature = current_temp
        self.pressure = current_pressure
        self.humidity = current_humid
        self._validate()
    
    def _validate(self):
        if not isinstance(self.temperature, float) or not isinstance(self.pressure, float) or not isinstance(self.humidity, float):
            print("Invalid sensor data") #i.e. GIVE ME ALL THE DATA (this is just a presense check, suggest change in future 31/10/23 11:40)
            self.temperature = 18
            self.pressure = 1013
            self.humidity = 45
            self.error = "Invalid sensor data"

def readings():
    temperature = CPU_temp - sense.get_temperature()
    pressure = sense.get_pressure()
    humidity = sense.get_humidity()
    value = CurrentReadings(temperature, pressure, humidity)
    return(value)

with open(filename,"w") as sensor_output:
        sensor_output.write("time,\t joy stick event,\t time_values (weekday,\t date(DD/MM/YYYY),\t time(HH:MM),\t sensor_data,\
                            \t temperature,\t pressure,\t humidity,\t error), \t iteration")

def sensor_output_file(iteration_count):
    sensor_data = readings()
    time_value = time_values()
    stick_data = sense.stick.get_events()
    try:
        stick_data = stick_data[0]
    except Exception as error:
        stick_data = error
        pass
    with open(filename,"a") as sensor_output:
        sensor_output.write(time_value.full_time + "\t stick event\t " + stick_data + "\t time_values\t " + time_value.day +"\t"+ time_value.date +"\t"+ \
                            time_value.time+"\t sensor_data \t" + sensor_data.temperature +"\t"+ sensor_data.pressure +"\t"+ sensor_data.humidity +"\t"+ \
                            sensor_data.error +"\t"+ iteration_count)
    return(0)
        
def time_output():
    time_value = time_values()
    ws(time_value.day)
    sleep(1)
    ws(time_value.date)
    sleep(1)
    ws(time_value.time)
    return(time_value.error)

def sensor_output():
    sensor_values = readings()
    ws("temperature " + str(int(sensor_values.temperature)))
    sleep(1)
    ws("pressure " + str(int(sensor_values.pressure)))
    sleep(1)
    ws("humidity " + str(int(sensor_values.humidity)) + "%")


while True:
    event = sense.stick.get_events()
    movment = sense.accelerometer
    # if is_pressed("C"):
    #     break
    try: # because this is not always pressed it can and does error when no data input.

        print(event[0].direction) # the variable event is a array what holds objects that can be called be calling... 
        if event[0].direction == "up": # ..a point in the array and then the value wanted from the ditionary
            time_output()
        
        if event[0].direction == "down":
            sensor_output()
            
    except KeyboardInterrupt as e:
        print(e)
        break
    except Exception as e: # outputs the error message when an error state happens
        print(e)

    try:
        if movment["roll"] ==  movment_old["roll"]:
            print(movment["roll"])
    except Exception as e:
        print(e)
    
    movment_old = movment
    iteration_count += 1
    sensor_output_file(iteration_count)
    print(iteration_count)
    sleep(1)