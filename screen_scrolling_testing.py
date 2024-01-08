from time import sleep
import numpy as np
import json
from file_of_greatness import system_check, logger

sense = system_check()

RED = (0, 255, 0)
BLUE = (0, 0, 255)
#test_setup()
matrix = np.full((8,8,3), BLUE) #[[BLUE for column in range(8)] for row in range(8)]

def flatten(matrix):
    return matrix.reshape(-1,3)

colour = BLUE
clear = (0,0,0)

FC = colour                                          #START LOWER CASE UNLESS ROUND WHEN GO 1 TALLER
OO = clear

with open("letters.json", "r") as letters_json:
    letters = json.load(letters_json)

BLUE = (0, 0, 255) #callable veriable for colour blue
ALL_BLUE = np.full((8, 8, 3), BLUE) #creates an 8x8x3 array that can then store BLUE (0,0,255) in each 8x8 slot
ALL_CLEAR = np.full((8,8,3),clear)
matrix = ALL_CLEAR.copy() #copys the data in the memory location assosiated with the all_blue veriable


def word_scrolling(text):
    word_list = ALL_CLEAR.copy()#np.full((8, 8, 3), RED)

    for character in text:
        try:
            word_list = np.append(word_list, letters[character], axis=1)
        except Exception as e:
            print(e)
    
    word_list = np.append(word_list, ALL_CLEAR, axis=1)

    COLUMNS_IN_SCREEN = 8

    total_columns = len(word_list[0])-7
    # Loop through frames
    for frame in range(total_columns):
        # Set each physical column for every frame
        for physical_column in range(COLUMNS_IN_SCREEN):
            # Invert column ordering because 0,0 is top right
            matrix[physical_column, :] = word_list[:, 7 - physical_column + frame]
        
        sense.set_pixels(flatten(matrix))
        sleep(0.05)


def test_setup():
    """ensures that the dysplay is working correctly"""
    sense.set_pixel(7,7,255,0,255)#x,y,R,G,B
    sense.set_pixel(0,0,255,0,0)#X goes parallel to the usb ports and tangent to the GPIOs
    sense.set_pixel(0,2,255,0,255)#Y goes along side the GPIO
    sense.set_pixel(2,0,0,255,0)
    sleep(2)
    word_scrolling("test underway ...")
    sleep(2)
    word_scrolling("... test complete")
    print("test complete")
    logger().warning("screen test performed")