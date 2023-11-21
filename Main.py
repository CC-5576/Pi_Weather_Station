'''Ollie Criddle, Threading for main code'''

import threading
from time import sleep
import WeatherStation as WS
from screen_scrolling_testing import word_scrolling as ws
from seismograph import seismograph
from file_of_greatness import system_check
sense = system_check()



def get_sensor_data():
    while True:
        # get data, apppend, etc
        event = sense.stick.get_events()
        movment = sense.accelerometer

        try: # because this is not always pressed it can and does error when no data input.

            print(event[0].direction) # the variable event is a array what holds objects that can be called be calling... 
            if event[0].direction == "up": # ..a point in the array and then the value wanted from the ditionary
                WS.time_output()
            
            if event[0].direction == "down":
                WS.sensor_output()
                
        except Exception as e: # outputs the error message when an error state happens
            event = e
            print(e)

        try:
            if movment["roll"] ==  movment_old["roll"]:
                print(movment["roll"])
            quake_reading = seismograph(100)
            if "str" in type(quake_reading):
                print(quake_reading)
            else:
                ws(str(quake_reading))
        except Exception as e:
            print(e)
        
        WS.log(event)
        movment_old = movment
        iteration_count += 1
        print(iteration_count)
        sleep(1)
        pass
        

def do_check():
    while True:
        print("Doing check...")
        # do check on data
        sleep(1)

def do_log():
    while True:
        print("Logging...")
        sleep(10)
        

def handle_user_input(user_input):
    # do thing
    print("user_input")
    return

sensor_thread = threading.Thread(target=get_sensor_data)
sensor_thread.start()

maths_thread = threading.Thread(target=do_check)
maths_thread.start()

logging_thread = threading.Thread(target=do_log)
logging_thread.start()

while True:
    handle_user_input(input("input -> "))