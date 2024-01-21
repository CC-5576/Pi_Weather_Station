from file_of_greatness import system_check, logger, timeSubtraction as TS
from time import sleep, time
import datetime
from math import log
from letters_json_write import letters

logger = logger()

sense = system_check()

xyz_avg_data = [[],[]]
time_data = [] #current_time = datetime.datetime.now #current_time.hour/minute/second/microsecond #dt.datetime.now().time() returns only the time portion, find a way to subtract 2 of these

def setup():
    START_VALUE = sense.accelerometer_raw
    for i in range(0, 100):
        xyz_avg_data.append(mean(START_VALUE["x"] - sense.accelerometer_raw["x"],
        START_VALUE["y"] - sense.accelerometer_raw["y"],
        START_VALUE["z"] - sense.accelerometer_raw["z"]))
    print("calibrated")
    return(START_VALUE)

def mean(X,Y,Z):
    current = (X+Y+Z)/3
    return(current)

def data_collection(data_length = 7000, iterations = 1, START_VALUE = setup()):
    data = []
    for y in range(iterations):
        data = []
        with open("logs/2024-01-21QuakeTrainingData.log", "a") as logs:
            for x in range(data_length):
                data.append([mean(START_VALUE["x"] - sense.accelerometer_raw["x"],
                START_VALUE["y"] - sense.accelerometer_raw["y"],
                START_VALUE["z"] - sense.accelerometer_raw["z"])
                ,datetime.datetime.now().time()])
            logs.write(str(data))
            logs.close()
        print(data[0][1]<data[data_length-1][1])
        print(TS(data[0][1],data[data_length-1][1]))
    
    print("done")
    return(data)

def seismograph(DATA_LENGTH = 7000, START_VALUE = setup()):
    WEIGHT = 0.125 #in kg
    print("started")
    xyz_avg_data = data_collection(DATA_LENGTH,1,START_VALUE)
    
    print("data collected")

    High_peak = xyz_avg_data[0]
    Low_peak = xyz_avg_data[0]
    Low_peak_found = False
    High_peak_position = 0

    for i in range(1, DATA_LENGTH):
        if High_peak[0]**2 < xyz_avg_data[i][0]**2:
            High_peak = xyz_avg_data[i]
            High_peak_position = i

    for i in range(High_peak_position+1, DATA_LENGTH):
        if Low_peak_found == False:
            if Low_peak[0]**2 < xyz_avg_data[i][0]**2:
                Low_peak[0] = xyz_avg_data[i][0]
            if Low_peak[0]**2 > xyz_avg_data[i][0]**2:
                Low_peak = xyz_avg_data[i]
                Low_peak_found = True
        if Low_peak_found:
            break
    
    print("peaks found")

    HighTime = (((Low_peak[1].hour*60+Low_peak[1].minute)*60+Low_peak[1].second)*(10**6)+Low_peak[1].microsecond)
    lowTime = (((High_peak[1].hour*60+High_peak[1].minute)*60+High_peak[1].second)*(10**6)+High_peak[1].microsecond)

    time_between_peaks = (HighTime - lowTime)*(10**-6)
    print(time_between_peaks)
    if time_between_peaks == 0:
        return ("no quake detected")
    
    try:
        print(len(str(log((8*time_between_peaks), 10))))
        log_time = log((8*time_between_peaks), 10)
    except Exception as e:
        print(e)
        logger.warning(f"line 79 seismograph: {e} \ttime_between_peaks = {time_between_peaks[:10]}")
        log_time = 0

    distance_from_source = abs((3 * log_time - 2.92)*(8/5)*10**2) #abs returns positive value

    location_change = (High_peak[0]**2)**0.5

    richter_scale = log((WEIGHT*location_change)*distance_from_source, 10)
    richter_scale = abs((richter_scale-4.4)/1.5)

    if richter_scale < 0:
        return(0)
    else:
        return(richter_scale)
