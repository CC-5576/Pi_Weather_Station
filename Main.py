'''Ollie Criddle, Threading for main code'''

import threading
from time import sleep
import WeatherStation as WS
from screen_scrolling_testing import word_scrolling
from seismographV2 import seismograph
from file_of_greatness import system_check, file_iteration_count
from numpy import mean
sense = system_check()
iteration = 0

from file_of_greatness import system_check, logger
from time import sleep
from math import log
logger = logger()

sense = system_check()
backgroundNoiseValue = 0
backgroundNoiseValuesXYZ = {
    "x":0,
    "y":0,
    "z":0
}

DATA_LENGTH = 100
x_data = [0]*DATA_LENGTH
y_data = [0]*DATA_LENGTH
z_data = [0]*DATA_LENGTH
WEIGHT = 0.150 #in kg

def user_input():
    WS.main(0)
        


def seismograph_acctivator():
    sleep(3)
    while True:
        if mean([sense.accelerometer_raw["x"], sense.accelerometer_raw["y"], sense.accelerometer_raw["z"]]) > (backgroundNoiseValue*1.5):
            richter_scale = seismograph(backgroundNoiseValuesXYZ)

        try:
            if richter_scale != 0:
                if richter_scale != "no quake detected":
                    word_scrolling("tremmour felt measuring " + str(richter_scale))
            
            print(richter_scale)
        except Exception as e:
            print(e)


def backgroundNoise():
    newData = []
    newXYZ = [[],[],[]]
    for i in range(1000):
        newData.append(mean([sense.accelerometer_raw["x"], sense.accelerometer_raw["y"], sense.accelerometer_raw["z"]]))
        newXYZ[0].append(sense.accelerometer_raw["x"])
        newXYZ[1].append(sense.accelerometer_raw["y"])
        newXYZ[2].append(sense.accelerometer_raw["z"])

    backgroundNoiseValue = mean(newData)
    backgroundNoiseValuesXYZ["x"] = mean(newXYZ[0])
    backgroundNoiseValuesXYZ["y"] = mean(newXYZ[1])
    backgroundNoiseValuesXYZ["z"] = mean(newXYZ[2])
    sleep(60)
        

def handle_user_input(user_input):
    # do thing
    print("user_input")
    return()


maths_thread = threading.Thread(target=seismograph_acctivator)
maths_thread.start()

backgroundNoise_Thread = threading.Thread(target=backgroundNoise)
backgroundNoise_Thread.start()

logging_thread = threading.Thread(target=user_input)
logging_thread.start()

print("please start")