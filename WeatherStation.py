from sense_emu import SenseHat
from time import sleep
import numpy as np
import screen_scrolling_testing as SST
import datetime as DT
ws = SST.word_scrolling
Sense = SenseHat
time_current = str(DT.datetime.now().time())[:5]
date_current = DT.date.today()
Sense.get_temperature()

