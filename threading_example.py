import threading
from time import sleep

my_data = [(), ()]

def get_sensor_data():
    while True:
        my_data []
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
    print(user_input)
    return

sensor_thread = threading.Thread(target=get_sensor_data)
sensor_thread.start()

maths_thread = threading.Thread(target=do_check)
maths_thread.start()

logging_thread = threading.Thread(target=do_log)
logging_thread.start()

while True:
    handle_user_input(input("input -> "))