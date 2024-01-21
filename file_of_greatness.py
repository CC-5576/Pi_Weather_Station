#ollie Criddle 30/10/2023
#this file will contain any small imports or general set up lines that are used throughout my project
import platform
import logging as log
import datetime

def system_check():

    if "rpi" not in platform.release():
        try:
            from sense_emu import SenseHat
            print("Xbuntu compatible import has been selected")
        except:
            pass
    else:
        try:
            from sense_hat import SenseHat
            print("Rasberry Pi compatible import has been selected")
        except:
            pass

    Sense = SenseHat()
    return(Sense)

def CPU_temp():
    '''depending on the system it will either return 0 or '''
    if "rpi" not in platform.release():
        CPU_temp = 0
    else:
        try:
            from gpiozero import CPUTemperature
            CPU_temp = CPUTemperature().temperature
        except:
            CPU_temp = 0
    
    return(CPU_temp)

days_of_the_week = {
    "6": "Sunday",
    "5": "Saturday",
    "4": "Friday",
    "3": "Thursday",
    "2": "Wednesday",
    "1": "Tuesday",
    "0": "Monday"
}

def file_iteration_count():
    with open("logs/iteration_count", "r") as current_iteration:
        current_iteration = int(current_iteration.read())
        with open("logs/iteration_count", "w") as new_iteration:
            new_iteration.write(str(current_iteration+1))
    
    return(current_iteration)

'loggin tool'
def logger():
    FORMAT = '%(asctime)s %(message)s'
    log.basicConfig(filename="logs/WeatherStation.log", filemode="a", format=FORMAT)
    logger = log.getLogger('logs/WeatherStation.log')
    logger.warning("start up: %s", 'STARTING')
    return(logger)


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