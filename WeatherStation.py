'''Ollie Criddle Pi Weather Station Project Main Page'''
#imports
import platform
from CommonImports import system_check, logger
import datetime
import math

sensorDataLog = logger("logs/WeatherStation/Sensors.log")
sense = system_check()

#importing setting up constants that will be used later

iteration_count = 0
event_count = 0

days_of_the_week = {
    "6": "Sunday",
    "5": "Saturday",
    "4": "Friday",
    "3": "Thursday",
    "2": "Wednesday",
    "1": "Tuesday",
    "0": "Monday"
}

def CPU_temp():
    '''depending on the system it will either return 0 or the actual cpu temperature'''
    if "rpi" not in platform.release():
        CPU_temp = 0
    else:
        try:
            from gpiozero import CPUTemperature
            CPU_temp = CPUTemperature().temperature
        except:
            CPU_temp = 0
    
    return(CPU_temp)


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
    time_current = str(datetime.datetime.now().time().hour) + ":"+ str(datetime.datetime.now().time().minute)
    date_current = (str(datetime.date.today().year)+ "/"+ str(datetime.date.today().month)+ "/"+ str(datetime.date.today().day))
    day_current = str(datetime.date.today().weekday())
    full_time = str(datetime.datetime.now())
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
    message = f"Sensor_data(t,p,h,HI,DP): {sensor_data.temperature}, {sensor_data.pressure}, {sensor_data.humidity}, {sensor_data.heatindex}, {sensor_data.dewpoint} \tloop_iteration: {iteration_count} \tstick_event: {stick_data} \t CPU_temp: {CPU_temp()}"
    sensorDataLog.warning(message)
    print(message)
    

        
def time_output():
    '''Outputs the time values from the object time_values to the word scrolling module'''
    time_value = time_values()
    return(time_value.day + " " + time_value.date + " " + time_value.time)

def sensor_output():
    '''Outputs the temperature, pressure, humidity values from the object time_values to the word scrolling module'''
    sensor_values = readings_TPH()
    return("temperature " + str(int(sensor_values.temperature)) + " " + "pressure " + str(int(sensor_values.pressure)) + " " + "humidity " + str(int(sensor_values.humidity)) + "%")

def main(iteration_count = 0):
    # get data, apppend, etc
    event = sense.stick.get_events()

    try: # because this is not always pressed it can and does error when no data input.

        values = readings_TPH()
        if values.temperature > 30:
            return("warning, high temperature: " + values.temperature)
        
        if values.temperature < 5:
            return("warning, low temperature: " + values.temperature)
        
        #print(event[0].direction) # the variable event is a array what holds objects that can be called be calling... 
        if event[0].direction == "up": # ..a point in the array and then the value wanted from the ditionary
            return(time_output())
        
        if event[0].direction == "down":
            return(sensor_output())

        if event[0].direction == "left":
            return("Dewpoint:" + str(values.dewpoint) + "  Heat Index:" + str(values.heatindex))
            
    except Exception as e: # outputs the error message when an error state happens, this will heppen everytime the toggle is not moved as we are looking for a state that has not happend
        event = e

    if iteration_count%10 == 0:
        log(event)
    iteration_count += 1
    pass