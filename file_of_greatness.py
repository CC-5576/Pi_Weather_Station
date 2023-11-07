#ollie Criddle 30/10/2023
#this file will contain any small imports or general set up lines that are used throughout my project

import platform
import logging as log

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
    logger = log.getLogger('logs/WeatherStation_log')
    logger.warning("start up: %s", 'STARTING')
    return(logger)