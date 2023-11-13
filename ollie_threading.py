'''Ollie Criddle 13/11/2023 python threading
should allow me to run the earthquake detection 
software at the same time as the main code'''

import threading
import WeatherStation as WS

def printing():
    for i in range(20):
        print(i)

T1 = threading.thread(target=printing)
T2 = threading.thread(target=WS)

T1.start()
T2.start()

T1.join()
T2.join()

print("bob")