from file_of_greatness import system_check, logger
from time import sleep, time
from math import log
logger = logger()

sense = system_check()
xyz_avg_data = []
time_data = [] #current_time = datetime.datetime.now #current_time.hour/minute/second/microsecond #dt.datetime.now().time() returns only the time portion, find a way to subtract 2 of these

def setup():
    START_VALUE = sense.accelerometer_raw
    for i in range(0, 100):
        xyz_avg_data.append(mean(START_VALUE["x"] - sense.accelerometer_raw["x"],
        START_VALUE["y"] - sense.accelerometer_raw["y"],
        START_VALUE["z"] - sense.accelerometer_raw["z"]))
    print("calibrated")
    return START_VALUE

def mean(X,Y,Z):
    accelerometer_raw = {"x":X,"y":Y,"z":Z}
    current = (accelerometer_raw["X"]+accelerometer_raw["Y"]+accelerometer_raw["Z"])/3
    return(current)

def main():
    print("")

def seismograph(DATA_LENGTH):
    START_VALUE = setup()
    WEIGHT = 0.150 #in kg

    for i in range(0, DATA_LENGTH):
        xyz_avg_data[i] = mean(START_VALUE["x"] - sense.accelerometer_raw["x"],
        START_VALUE["y"] - sense.accelerometer_raw["y"],
        START_VALUE["z"] - sense.accelerometer_raw["z"])
        

    

    x_high_peak = xyz_avg_data[0]
    x_low_peak = xyz_avg_data[0][0]
    x_low_peak_found = False
    x_high_peak_position = 0
    x_low_peak_position = 0

    for i in range(0, DATA_LENGTH):
        if x_high_peak**2 < xyz_avg_data[i]**2:
            x_high_peak = xyz_avg_data[i]

    for i in range(0, DATA_LENGTH):
        if x_low_peak_found == False:
            if x_low_peak**2 < xyz_avg_data[i][0]**2:
                x_low_peak = xyz_avg_data[i][0]
                x_low_peak_position = i
            if x_low_peak**2 > xyz_avg_data[i][0]**2:
                x_low_peak_found = True
        if x_low_peak_found:
            break
    
    high_peak_position = x_high_peak_position
    low_peak_position = x_low_peak_position
    time_between_peaks = (high_peak_position-low_peak_position)*0.1
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

    location_change = (x_high_peak**2+y_high_peak**2+z_high_peak**2)**0.5

    richter_scale = log((WEIGHT*location_change)*distance_from_source, 10)
    richter_scale = (richter_scale-11.8)/1.5

    if richter_scale < 0:
        return(0)
    else:
        return(richter_scale)
    

"""
>>> dt.datetime.now().time
<built-in method time of datetime.datetime object at 0x7fa21a80c0>
>>> print(dt.datetime.now().time)
<built-in method time of datetime.datetime object at 0x7fa1f4bc00>
>>> bill = dt.datetime.now().time
>>> bill
<built-in method time of datetime.datetime object at 0x7fa2165c80>
>>> dt.datetime.now().time()
datetime.time(23, 22, 30, 294128)
>>> bill = dt.datetime.now().time()
>>> dave = dt.datetime.now().time()
>>> bill-dave
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for -: 'datetime.time' and 'datetime.time'
>>> def time_subtraction(old dt.time,new dt.time):
  File "<stdin>", line 1
    def time_subtraction(old dt.time,new dt.time):
                             ^^
SyntaxError: invalid syntax
>>> def time_subtraction(old,new):
...     current = datetime."""