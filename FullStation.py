'''Ollie Criddle, Threading for main code'''

import threading
from time import sleep
import WeatherStation as WS
from screen_scrolling_testing import word_scrolling
from seismographV2 import seismograph
from CommonImports import system_check, logger
from numpy import mean
from time import sleep
from math import log

iterations = 0
debugLog = logger("logs/FullStations/Debug.log")
seismicLog = logger("logs/FullStation/seismicReadings.log")
sense = system_check()
backgroundNoiseValue = 0
backgroundNoiseValuesXYZ = {
    "x":0,
    "y":0,
    "z":0,
    "i":0
}

DATA_LENGTH = 100
x_data = [0]*DATA_LENGTH
y_data = [0]*DATA_LENGTH
z_data = [0]*DATA_LENGTH
WEIGHT = 0.150 #in kg

def user_input():
    WS.main()
        


def seismograph_acctivator():
    sleep(3)
    while True:
        if mean([sense.accelerometer_raw["x"], sense.accelerometer_raw["y"], sense.accelerometer_raw["z"]]) > (backgroundNoiseValue*1.5):
            richter_scale = seismograph(7000, backgroundNoiseValuesXYZ)
            if richter_scale != 0:
                if richter_scale != "no quake detected":
                    word_scrolling("tremmour felt measuring " + str(richter_scale))
            
            print(richter_scale)
            seismicLog.warning(richter_scale)


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

    if backgroundNoiseValuesXYZ["i"]%50 == 0:
        seismicLog.warning(f"background noise: {backgroundNoiseValuesXYZ}")
    
    backgroundNoiseValuesXYZ["i"] += 1
    sleep(60)


maths_thread = threading.Thread(target=seismograph_acctivator)
backgroundNoise_Thread = threading.Thread(target=backgroundNoise)
user_controls = threading.Thread(target=user_input)

maths_thread.start()
backgroundNoise_Thread.start()
user_controls.start()

print("please start")