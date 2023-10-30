#ollie Criddle 30/10/2023
#this file will contain any small imports or general set up lines that are used throughout my project

def system_check():
    with open("info.read", 'r') as info:
        if info.read().__contains__("Xbuntu"):
            try:
                from sense_emu import SenseHat
                print("Xbuntu compatible import has been selected")
            except:
                pass
        else:
            from sense_hat import SenseHat
            print("Rasberry Pi compatible import has been selected")
        Sense = SenseHat
        return(Sense)