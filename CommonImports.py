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

'loggin tool'
def logger(filename = "logs/error.log"):
    FORMAT = '%(asctime)s %(message)s'
    log.basicConfig(filename=filename, filemode="a", format=FORMAT)
    logger = log.getLogger(filename)
    logger.warning("start up: %s", 'STARTING')
    return(logger)
