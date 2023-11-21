import threading
from time import sleep

my_data = [(1,2,3,4), (5,6,7,8)]

def get_sensor_data():
    while True:
        print("data")
        # get data, apppend, etc
        sleep
        pass
        

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