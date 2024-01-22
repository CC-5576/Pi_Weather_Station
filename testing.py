from FullStation import system_check as sense
from datetime import datetime as dt
import datetime

def timesubtraction(older, newer):
        oldtime = (((older.hour*60+older.minute)*60+older.second)*(10**6)+older.microsecond)
        newtime = (((newer.hour*60+newer.minute)*60+newer.second)*(10**6)+newer.microsecond)

        old= newtime-oldtime

        old = old/(60*60*10**6)
        hours = int(old)

        old = (old - hours)*60
        minutes = int(old)

        old = (old-minutes)*60
        seconds = int(old)

        old = (old-seconds) * (10**6)
        microseconds = int(old)
        return(datetime.time(hours, minutes, seconds, microseconds))

def average(list):
    time = 0
    for x in list:
        time += (((x.hour*60+x.minute)*60+x.second)*(10**6)+x.microsecond)
    
    time = time/len(list)

    old = time/(60*60*10**6)
    hours = int(old)

    old = (old - hours)*60
    minutes = int(old)

    old = (old-minutes)*60
    seconds = int(old)

    old = (old-seconds) * (10**6)
    microseconds = int(old)

    return(datetime.time(hours, minutes, seconds, microseconds))

def main(iterations = 11, data_length = 100*10):
    avgTotalTime = []
    avgGatherTime = []

    for y in range(1,iterations+1):
        data = []
        with open("logs/2024-01-20-TimingTests.log", "w") as logs:
            for x in range(data_length):
                # data[0].append(sense.accelerometer_raw["x"])
                # data[1].append(dt.now().time())
                data.append([sense().accelerometer_raw["x"], dt.now().time()])
            logs.write(str(data))
            logs.close()
        
        gatherTime = []
        for x in range(data_length-1):
            gatherTime.append(timesubtraction(data[x][1], data[x+1][1]))
        print(data[0][1]<data[data_length-1][1], y)
        avgTotalTime.append(timesubtraction(data[0][1],data[data_length-1][1]))
        print(avgTotalTime[len(avgTotalTime)-1])
        avgGatherTime.append(average(gatherTime))
        print(avgGatherTime[len(avgTotalTime)-1])

    print(average(avgTotalTime), "Total Time Avg")
    print(average(avgGatherTime), "Gather Time Avg")

main(1,5)