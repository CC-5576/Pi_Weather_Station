'''Ollie Criddle, Threading for main code'''

import threading
from time import sleep
import WeatherStation as WS
from screen_scrolling_testing import word_scrolling
from seismograph import seismograph
from file_of_greatness import system_check, file_iteration_count
from numpy import mean
sense = system_check()
iteration = 0

from file_of_greatness import system_check, logger
from time import sleep
from math import log
logger = logger()

sense = system_check()


DATA_LENGTH = 100
x_data = [0]*DATA_LENGTH
y_data = [0]*DATA_LENGTH
z_data = [0]*DATA_LENGTH
WEIGHT = 0.150 #in kg

def get_acceloration_data():
    if x_data.count != 100 and y_data.count != 100 and z_data.count != 100:
        x_data.append(sense.accelerometer_raw["x"])
        y_data.append(sense.accelerometer_raw["y"])
        z_data.append(sense.accelerometer_raw["z"])
        
    else:
        x_data.pop(0)
        y_data.pop(0)
        z_data.pop(0)
        x_data.append(sense.accelerometer_raw["x"])
        y_data.append(sense.accelerometer_raw["y"])
        z_data.append(sense.accelerometer_raw["z"])
    
    x_high_peak = max(x_data)
    y_high_peak = max(y_data)
    z_high_peak = max(z_data)

    x_low_peak = min(x_data)
    y_low_peak = min(y_data)
    z_low_peak = min(z_data)
    
    x_high_peak_position = x_data.index(x_high_peak)
    y_high_peak_position = y_data.index(y_high_peak)
    z_high_peak_position = z_data.index(z_high_peak)
    x_low_peak_position = x_data.index(x_low_peak)
    y_low_peak_position = y_data.index(y_low_peak)
    z_low_peak_position = z_data.index(z_low_peak)

    
    high_peak_position = (x_high_peak_position + y_high_peak_position + z_high_peak_position)/3
    low_peak_position = (x_low_peak_position + y_low_peak_position + z_low_peak_position)/3
    time_between_peaks = (high_peak_position-low_peak_position)*0.1
    print(time_between_peaks)

    if time_between_peaks == 0:
        return ("no quake detected")
    
    difference = 1.5
    if x_high_peak >  (difference + mean(x_data)) or y_high_peak >  (difference + mean(y_data)) or z_high_peak >  (difference + mean(z_data)):
    
        try:
            print(len(str(log((8*time_between_peaks), 10))))
            log_time = log((8*time_between_peaks), 10)
            distance_from_source = abs((3 * log_time - 2.92)*(8/5)*10**2) #abs returns positive value

            location_change = (x_high_peak**2+y_high_peak**2+z_high_peak**2)**0.5

            richter_scale = log((WEIGHT*location_change)*distance_from_source, 10)
            richter_scale = (richter_scale-11.8)/1.5
        except Exception as e:
            print(e)
            logger.warning(f"line 79 seismograph: {e} \ttime_between_peaks = {str(time_between_peaks)[:10]}")
            richter_scale = -1

        if richter_scale < 0:
            return(0)
        else:
            return(richter_scale)

def user_input():
    WS.main(0)
        


def seismograph():
    sleep(3)
    while True:
        richter_scale = get_acceloration_data()
        if richter_scale != 0:
            if richter_scale != "no quake detected":
                word_scrolling("tremmour felt measuring " + str(richter_scale))
        
        print(richter_scale)

        

def handle_user_input(user_input):
    # do thing
    print("user_input")
    return()


maths_thread = threading.Thread(target=seismograph)
maths_thread.start()

logging_thread = threading.Thread(target=user_input)
logging_thread.start()

print("please start")