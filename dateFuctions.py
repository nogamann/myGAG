import time

def printTime(unix):
    mytime = time.gmtime(int(unix))
    return time.strftime("%a, %d %m %Y", mytime)


def printAllDates(df):
    for index, row in df.iterrows():
        for i in row['availability']:
            start = i['start']
            end = i['end']
            days = (end-start)/86400
            print(printTime(i['start']) + " to " + printTime(i['end']) + " - " + str(int(days)))

