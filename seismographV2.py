from CommonImports import system_check, logger
import datetime
from math import log

DebugLog = logger("logs/seismograph/Debug.log")
HistoricalData = logger("logs/seismograph/historicalData.log")

sense = system_check()

xyz_avg_data = [[],[]]
time_data = [] #current_time = datetime.datetime.now #current_time.hour/minute/second/microsecond #dt.datetime.now().time() returns only the time portion, find a way to subtract 2 of these

def setup():
    START_VALUE = sense.accelerometer_raw
    for i in range(0, 100):
        xyz_avg_data.append(mean(START_VALUE["x"] - sense.accelerometer_raw["x"],
        START_VALUE["y"] - sense.accelerometer_raw["y"],
        START_VALUE["z"] - sense.accelerometer_raw["z"]))
    print("seismograph calibrated")
    return(START_VALUE)

def mean(X,Y,Z):
    current = (X+Y+Z)/3
    return(current)

def data_collection(data_length = 7000, iterations = 1, START_VALUE = setup()):
    data = []
    for y in range(iterations):
        data = []
        for x in range(data_length):
            data.append([mean(START_VALUE["x"] - sense.accelerometer_raw["x"],
            START_VALUE["y"] - sense.accelerometer_raw["y"],
            START_VALUE["z"] - sense.accelerometer_raw["z"])
            ,datetime.datetime.now().time()])
            
            if x%int(data_length/100) == 0: #shows something is happening
                print(x)
        
        HistoricalData.warning(str(data))
        HistoricalData.warning(f"Time Taken For Collection: {(timeSubtraction(data[0][1],data[data_length-1][1]))}")
        print(timeSubtraction(data[0][1],data[data_length-1][1]))
    
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
        DebugLog.warning(f"line 79 seismograph: {e} \ttime_between_peaks = {time_between_peaks[:10]}")
        log_time = 0

    distance_from_source = abs((3 * log_time - 2.92)*(8/5)*10**2) #abs returns positive value

    location_change = (High_peak[0]**2)**0.5

    richter_scale = log((WEIGHT*location_change)*distance_from_source, 10)
    richter_scale = abs((richter_scale-4.4)/1.5)

    if richter_scale < 0:
        return(0)
    else:
        return(richter_scale)

def timeSubtraction(older, newer):
        """using the datetime.time() format, this function will subtract the two 
        times to output a positive number always subtracting the earlier time"""
        #checks that the newer time is infact the newer time (issues would arrise if the quake happened as the date changes, 
        #this could be fixed by changing it to use the datetime format rather than just time, or by using epoc time)
        if older > newer:
            tempTime = older
            older = newer
            newer = tempTime

        #turns the given data into microseconds
        oldtime = (((older.hour*60+older.minute)*60+older.second)*(10**6)+older.microsecond)
        newtime = (((newer.hour*60+newer.minute)*60+newer.second)*(10**6)+newer.microsecond)

        old = newtime-oldtime

        #changes the time back into hours to turn it back into the datetime.time() format
        old = old/(60*60*10**6)
        hours = int(old)

        old = (old - hours)*60
        minutes = int(old)

        old = (old-minutes)*60
        seconds = int(old)

        old = (old-seconds) * (10**6)
        microseconds = int(old)
        return(datetime.time(hours, minutes, seconds, microseconds))