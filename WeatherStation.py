'''Ollie Criddle Pi Weather Station Project Main Page'''
#imports
from time import sleep
from screen_scrolling_testing import word_scrolling, test_setup as ts # importing my screen scrolling code
import datetime as DT # importing the datetime module
from seismographV2 import seismograph
import math

from file_of_greatness import system_check, days_of_the_week, file_iteration_count, logger, CPU_temp
file_iteration_count = file_iteration_count()
sense = system_check()
print("why")
#logger()
logger = logger()
#importing setting up constants that will be used later

iteration_count = 0
event_count = 0
#setting up iteration count of this file and event counter for the trigger


sleep(1)
#ts() #testing the screen outout

class CurrentTime:
    """returns the current time, date, day, full_time values in an object"""
    '''used to create an object for ease of calling and pasing the new data,
    including checks to see if present'''
    #could expand to include type or format checking?
    def __init__(self, time, date, day, full_time):
        self.time = time
        self.day = day
        self.date = date
        self.full_time = full_time
        self.error = "Passed"
        self._validate()

    def _validate(self):
        if not isinstance(self.time, str) or not isinstance(self.day, str) or not isinstance(self.date, str):
            print("Invalid time object") #i.e. GIVE ME ALL THE DATA
            self.time = "00:00"
            self.day = "Monday"
            self.date = "1970/01/01"
            self.error = "Invalid time object"

def time_values():
    '''collects the time values and uses the above class to generate and return an object containing them'''
    time_current = str(DT.datetime.now().time().hour) + ":"+ str(DT.datetime.now().time().minute)
    date_current = (str(DT.date.today().year)+ "/"+ str(DT.date.today().month)+ "/"+ str(DT.date.today().day))
    day_current = str(DT.date.today().weekday())
    full_time = str(DT.datetime.now())
    day_current = days_of_the_week[day_current]
    value = CurrentTime(time_current, date_current, day_current, full_time)
    return(value)


class CurrentReadings:
    """returns the current temp, pressure, humidity readings in an object"""
    '''used to create an object for ease of calling and pasing the new data,
    including checks to see if present'''
    #could expand to include type or format checking?
    def __init__(self, current_temp, current_pressure, current_humid):
        self.temperature = current_temp
        self.pressure = current_pressure
        self.humidity = current_humid
        self.heatindex = ((-42.379 + 2.04901523*(self.temperature*(9/5)+32) + 10.14333127*self.humidity - .22475541*(self.temperature*(9/5)+32)*self.humidity - .00683783*(self.temperature*(9/5)+32)*(self.temperature*(9/5)+32) - .05481717*self.humidity*self.humidity + .00122874*(self.temperature*(9/5)+32)*(self.temperature*(9/5)+32)*self.humidity + .00085282*(self.temperature*(9/5)+32)*self.humidity*self.humidity - .00000199*(self.temperature*(9/5)+32)*(self.temperature*(9/5)+32)*self.humidity*self.humidity)-32)*(5/9)
        #https://www.toppr.com/guides/physics-formulas/heat-index-formula/
        self.dewpoint = (237.3*((math.log(self.humidity/100)+((17.27*self.temperature)/(237.3+self.temperature)))/17.27))/(1-((math.log(self.humidity/100)+((17.27*self.temperature)/(237.3+self.temperature)))/17.27))
        #https://ag.arizona.edu/azmet/dewpoint.html
        self._validate()
    
    def _validate(self):
        if not isinstance(self.temperature, float) or not isinstance(self.pressure, float) or not isinstance(self.humidity, float):
            print("Invalid sensor data") #i.e. GIVE ME ALL THE DATA (this is just a presense check, suggest change in future 31/10/23 11:40)
            self.temperature = 18
            self.pressure = 1013
            self.humidity = 45
            self.error = "Invalid sensor data"


def readings_TPH():
    '''Collects the Temperature, Pressure and Humidity and uses the above class to generate and return an object containing them'''
    temperature = CPU_temp() - sense.get_temperature()
    pressure = sense.get_pressure()
    humidity = sense.get_humidity()
    value = CurrentReadings(temperature, pressure, humidity)
    return(value)

def log(stick_data):
    '''logs all current sensor readings as gathered by reading_TMP'''
    sensor_data = readings_TPH()
    #print("I run")
    logger.warning(f"file_iteration: {file_iteration_count} \tSensor_data(t,p,h,HI,DP): {sensor_data.temperature}, {sensor_data.pressure}, {sensor_data.humidity}, {sensor_data.headindex}, {sensor_data.dewpoint} \tloop_iteration: {iteration_count} \tstick_event: {stick_data}")
    print((f"file_iteration: {file_iteration_count} \tSensor_data(t,p,h): {sensor_data.temperature}, {sensor_data.pressure}, {sensor_data.humidity} \tloop_iteration: {iteration_count} \tstick_event: {stick_data}"))

        
def time_output():
    '''Outputs the time values from the object time_values to the word scrolling module'''
    time_value = time_values()
    word_scrolling(time_value.day)
    sleep(1)
    word_scrolling(time_value.date)
    sleep(1)
    word_scrolling(time_value.time)
    return(time_value.error)

def sensor_output():
    '''Outputs the temperature, pressure, humidity values from the object time_values to the word scrolling module'''
    sensor_values = readings_TPH()
    word_scrolling("temperature " + str(int(sensor_values.temperature)), 15)
    sleep(1)
    word_scrolling("pressure " + str(int(sensor_values.pressure)), 15)
    sleep(1)
    word_scrolling("humidity " + str(int(sensor_values.humidity)) + "%", 15)

def main(iteration_count = 0):
    while True:
            # get data, apppend, etc
            event = sense.stick.get_events()
            movment = sense.accelerometer

            try: # because this is not always pressed it can and does error when no data input.

                if readings_TPH().temperature > 20:
                    word_scrolling("WARNING, HIGH TEMPERATURE")
                
                if readings_TPH().temperature < 5:
                    word_scrolling("WARNING, LOW TEMPERATURE")
                
                #print(event[0].direction) # the variable event is a array what holds objects that can be called be calling... 
                if event[0].direction == "up": # ..a point in the array and then the value wanted from the ditionary
                    time_output()
                
                if event[0].direction == "down":
                    sensor_output()

                if event[0].direction == "left":
                    values = readings_TPH()
                    word_scrolling("Dewpoint:" + str(values.dewpoint), 15)
                    word_scrolling("Heat Index:" + str(values.heatindex), 10)
                    

            except Exception as e: # outputs the error message when an error state happens
                event = e
                #print(e)

            
            if iteration_count%10 == 0:
                log(event)
            iteration_count += 1
            #print(iteration_count)
            sleep(1)
            pass