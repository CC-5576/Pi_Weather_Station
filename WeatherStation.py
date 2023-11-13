'''Ollie Criddle Pi Weather Station Project Main Page'''
#imports
from time import sleep
from screen_scrolling_testing import word_scrolling as ws, test_setup as ts # importing my screen scrolling code
import datetime as DT # importing the datetime module
from seismograph import seismograph


from file_of_greatness import system_check, days_of_the_week, file_iteration_count, logger, CPU_temp
file_iteration_count = file_iteration_count()
sense = system_check()
#importing setting up constants that will be used later

iteration_count = 0
event_count = 0
#setting up iteration count of this file and event counter for the trigger


sleep(1)
ts() #testing the screen outout

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
    logger().warning(f"file_iteration: {file_iteration_count} \tSensor_data(t,p,h): {sensor_data.temperature}, {sensor_data.pressure}, {sensor_data.humidity} \tloop_iteration: {iteration_count} \tstick_event: {stick_data}")
    print((f"file_iteration: {file_iteration_count} \tSensor_data(t,p,h): {sensor_data.temperature}, {sensor_data.pressure}, {sensor_data.humidity} \tloop_iteration: {iteration_count} \tstick_event: {stick_data}"))

        
def time_output():
    '''Outputs the time values from the object time_values to the word scrolling module'''
    time_value = time_values()
    ws(time_value.day)
    sleep(1)
    ws(time_value.date)
    sleep(1)
    ws(time_value.time)
    return(time_value.error)


def sensor_output():
    '''Outputs the temperature, pressure, humidity values from the object time_values to the word scrolling module'''
    sensor_values = readings_TPH()
    ws("temperature " + str(int(sensor_values.temperature)))
    sleep(1)
    ws("pressure " + str(int(sensor_values.pressure)))
    sleep(1)
    ws("humidity " + str(int(sensor_values.humidity)) + "%")


while True:
    event = sense.stick.get_events()
    movment = sense.accelerometer
    # if is_pressed("C"):
    #     break
    try: # because this is not always pressed it can and does error when no data input.

        print(event[0].direction) # the variable event is a array what holds objects that can be called be calling... 
        if event[0].direction == "up": # ..a point in the array and then the value wanted from the ditionary
            time_output()
        
        if event[0].direction == "down":
            sensor_output()
            
    except Exception as e: # outputs the error message when an error state happens
        event = e
        print(e)

    try:
        if movment["roll"] ==  movment_old["roll"]:
            print(movment["roll"])
        quake_reading = seismograph(100)
        if "str" in type(quake_reading):
            print(quake_reading)
        else:
            ws(str(quake_reading))
    except Exception as e:
        print(e)
    
    log(event)
    movment_old = movment
    iteration_count += 1
    print(iteration_count)
    sleep(1)