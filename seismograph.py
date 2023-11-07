from file_of_greatness import system_check, logger
from time import sleep
from math import log
logger = logger()

sense = system_check()

def setup():
    START_VALUE = sense.accelerometer_raw
    print("calibrated")
    return START_VALUE

START_VALUE = setup()

def seismograph(DATA_LENGTH, START_VALUE):
    WEIGHT = 0.150 #in kg


    xyz_data = [[0]*3]*DATA_LENGTH
    for i in range(0, DATA_LENGTH):
        xyz_data[i][0] = START_VALUE["x"] - sense.accelerometer_raw["x"]
        xyz_data[i][1] = START_VALUE["y"] - sense.accelerometer_raw["y"]
        xyz_data[i][2] = START_VALUE["z"] - sense.accelerometer_raw["z"]
        

    

    x_high_peak = xyz_data[0][0]
    y_high_peak = xyz_data[0][1]
    z_high_peak = xyz_data[0][2]
    x_low_peak = xyz_data[0][0]
    y_low_peak = xyz_data[0][1]
    z_low_peak = xyz_data[0][2]
    x_low_peak_found = False
    y_low_peak_found = False
    z_low_peak_found = False
    x_high_peak_position = 0
    y_high_peak_position = 0
    z_high_peak_position = 0
    x_low_peak_position = 0
    y_low_peak_position = 0
    z_low_peak_position = 0

    for i in range(0, DATA_LENGTH):
        if x_high_peak**2 < xyz_data[i][0]**2:
            x_high_peak = xyz_data[i][0]
            x_high_peak_position = i
        if y_high_peak**2 < xyz_data[i][0]**2:
            y_high_peak = xyz_data[i][0]
            y_high_peak_position = i
        if z_high_peak**2 < xyz_data[i][1]**2:
            z_high_peak = xyz_data[i][2]
            z_high_peak_position = i

    for i in range(0, DATA_LENGTH):
        if x_low_peak_found == False:
            if x_low_peak**2 < xyz_data[i][0]**2:
                x_low_peak = xyz_data[i][0]
                x_low_peak_position = i
            if x_low_peak**2 > xyz_data[i][0]**2:
                x_low_peak_found = True
        if y_low_peak_found == False:
            if y_low_peak**2 < xyz_data[i][0]**2:
                y_low_peak = xyz_data[i][0]
                y_low_peak_position = i
            if y_low_peak**2 > xyz_data[i][0]**2:
                y_low_peak_found = True
        if z_low_peak_found == False:
            if z_low_peak**2 < xyz_data[i][0]**2:
                z_low_peak = xyz_data[i][0]
                z_low_peak_position = i
            if z_low_peak**2 > xyz_data[i][0]**2:
                z_low_peak_found = True
        if x_low_peak_found and y_low_peak_found and z_low_peak_found:
            break
    
    high_peak_position = (x_high_peak_position + y_high_peak_position + z_high_peak_position)/3
    low_peak_position = (x_low_peak_position + y_low_peak_position + z_low_peak_position)/3
    time_between_peaks = (high_peak_position-low_peak_position)*0.03
    print(time_between_peaks)
    try:
        print(len(str(log((8*time_between_peaks), 10))))
        log_time = log((8*time_between_peaks), 10)
    except Exception as e:
        print(e)
        logger.warning(f"line 79 seismograph: {e} \ttime_between_peaks = {time_between_peaks}")
        log_time = 0

    distance_from_source = abs((3 * log_time - 2.92)*(8/5)*10**2) #abs returns positive value

    location_change = (x_high_peak**2+y_high_peak**2+z_high_peak**2)**0.5

    richter_scale = log((WEIGHT*location_change)*distance_from_source, 10)
    richter_scale = (richter_scale-11.8)/1.5

    if richter_scale < 0:
        return(0)
    else:
        return(richter_scale)

print(seismograph(100, START_VALUE))