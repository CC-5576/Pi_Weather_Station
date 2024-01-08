'''Ollie Criddle, Threading for main code'''

import threading
from time import sleep
import WeatherStation as WS
from screen_scrolling_testing import word_scrolling as ws
from seismograph import seismograph
from file_of_greatness import system_check, file_iteration_count
sense = system_check()
iteration = 0


def get_sensor_data():
    WS.main()
        

def do_check():
    while True:
        print("Doing check...")
        # do check on data
        sleep(1)

def do_log():
    while True:
        print("Logging...")
        sleep(10)
        

def handle_user_input(user_input):
    # do thing
    print("user_input")
    return

sensor_thread = threading.Thread(target=get_sensor_data)
sensor_thread.start()

maths_thread = threading.Thread(target=do_check)
maths_thread.start()

logging_thread = threading.Thread(target=do_log)
logging_thread.start()

while True:
    handle_user_input(input("input -> "))