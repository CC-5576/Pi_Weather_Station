'''Ollie Criddle, Threading for main code'''

import threading
from time import sleep
import WeatherStation as WS
from screen_scrolling_testing import word_scrolling
from seismographV2 import seismograph
from CommonImports import system_check, logger
from numpy import mean

start = False
textOut = False
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

messageList = []

def screenOutput():
    ScreenOutIteration = 0
    textOut = False
    while True:
        try:
            if textOut == False:
                textOut = True
                word_scrolling(messageList.pop(0), 15)
                textOut = False
        except Exception as e:
            if ScreenOutIteration%600 == 0:
                print(e)

        print("screen output check: " + str(ScreenOutIteration))
        ScreenOutIteration += 1
        sleep(1)

def user_input():
    iteration_count = 0
    while True:
        message = WS.main(iteration_count)
        if message != None:
            messageList.append(message)
        iteration_count += 1
        


def seismograph_acctivator():
    while start == False:
        pass

    print("activator started")
    messageList.append("activator started")
    while True:
        if mean([sense.accelerometer_raw["x"], sense.accelerometer_raw["y"], sense.accelerometer_raw["z"]]) > (backgroundNoiseValue*1.5):
            richter_scale = seismograph(7000, backgroundNoiseValuesXYZ)
            if richter_scale != 0:
                if richter_scale != "no quake detected":
                    messageList.append("tremmour felt measuring " + str(richter_scale))
            
            print(richter_scale)
            seismicLog.warning(richter_scale)


def backgroundNoise():
    print("background started")
    messageList.append("background started")
    while True:
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

        start = True
        if backgroundNoiseValuesXYZ["i"]%50 == 0:
            seismicLog.warning(f"background noise: {backgroundNoiseValuesXYZ}")
        
        backgroundNoiseValuesXYZ["i"] += 1
        sleep(60)


maths_thread = threading.Thread(target=seismograph_acctivator)
backgroundNoise_Thread = threading.Thread(target=backgroundNoise)
user_controls = threading.Thread(target=user_input)
output_thread = threading.Thread(target=screenOutput)

user_controls.start()
backgroundNoise_Thread.start()
maths_thread.start()
output_thread.start()

print("please start")