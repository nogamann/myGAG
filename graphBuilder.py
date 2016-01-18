import networkx as nx
import pandas as pd
from buildPickle import *
import threading
from dateFuctions import *

DAY = 86400

def buildGraph(listingsDF, startDate, endDate):
    startDate = toBaseDate(startDate)
    endDate = toBaseDate(endDate)
    graph = nx.DiGraph()
    graph.add_node('start',id='start',date=startDate,price=0,jumpable=0, priceweek=0)
    graph.add_node('end',id = 'end',date=endDate,price=0,jumpable=0, priceweek=0)
    numOfdays = int((endDate - startDate)/DAY + 1)
    hashtable = [[]]
    for i in range(numOfdays+1):
        hashtable.append([])
    hashtable[0].append('start')
    hashtable[numOfdays].append('end')
    for index, listing in listingsDF.iterrows():
        id=listing['id']
        for i in listing['availability']:
            start = i['start']
            end = i['end']
            curDates = splitToDays(start, end)
            canJumpWeek = len(curDates) - 7
            for index, date in enumerate(curDates):
                if date >= startDate:
                    if date >= endDate:
                        break
                    hashDate = int((date - startDate)/DAY) + 1
                    name = str(id) + "-" + str(date)
                    setJump = index <= canJumpWeek
                    graph.add_node(name,id=listing['id'],price=listing['price']['nightly'],priceweek = listing['price']['weekly'],date=date, jumpable=setJump)
                    hashtable[hashDate].append(name)
    for i in range(numOfdays+1):
        for first in hashtable[i]:
            firstNode = graph.node[first]
            for scnd in hashtable[i+1]:
                w = graph.node[scnd]['price']
                graph.add_edge(first,scnd,weight=w)
            if firstNode['jumpable']:
                date = firstNode['date'] + DAY*7
                name = str(firstNode['id']) + '-' + str(date)
                graph.add_edge(first,name,weight=firstNode['priceweek'])
    return graph


def buildGraphMultiThreading(picklePath, startDate, endDate):
    startDate = toBaseDate(startDate)
    endDate = toBaseDate(endDate)
    graph = nx.DiGraph()
    graph.add_node('start',id='start',date=startDate,price=0)
    graph.add_node('end',id = 'end',date=endDate,price=0)
    numOfdays = int((endDate - startDate)/DAY + 1)
    hashtable = [[]]


    for i in range(numOfdays+1):
        hashtable.append([])
    hashtable[0].append('start')
    hashtable[numOfdays].append('end')
    listings = readPickle(picklePath)
    for index, listing in listings.iterrows():
        id=listing['id']
        for i in listing['availability']:
            start = i['start']
            end = i['end']
            curDates = splitToDays(start, end)
            for date in curDates:
                if date >= startDate:
                    if date >= endDate:
                        break
                    hashDate = int((date - startDate)/DAY) + 1
                    name = str(id) + "-" + str(date)
                    graph.add_node(name,id=listing['id'],price=listing['price']['nightly'],date=date)
                    hashtable[hashDate].append(name)

    #
    #
    # for i in range(numOfdays+1):
    #     hashtable.append([])
    # hashtable[0].append('start')
    # hashtable[numOfdays].append('end')
    # listings = readPickle(picklePath)
    # listings = listings.reset_index()
    # numOfListings = len(listings.index)
    # threadNum = 2
    # threads = []
    # gap = numOfListings//threadNum
    # print('heyyy')
    # for i in range(threadNum):
    #     startIndex = i*gap
    #     endIndex = startIndex + gap
    #     thread = threading.Thread(target=graphMultithreadingHelper1, args=(hashtable,graph, startDate, endDate, startIndex, endIndex, listings))
    #     threads.append(thread)
    #     thread.start()
    # for thread in threads:
    #     thread.join()
    # print('byeeee')
    threadNum =2
    threads = []
    gap = len(hashtable)//threadNum
    for i in range(threadNum):
        startIndex = i*gap
        endIndex = startIndex + gap
        thread = threading.Thread(target=graphMultithreadingHelper2, args=(hashtable,graph, startIndex, endIndex))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    return graph

def graphMultithreadingHelper1(hashtable, graph, startDate, endDate, startIndex, endIndex, df):
    for index in range(startIndex, endIndex):
            id=df.loc[index]['id']
            for i in df.loc[index]['availability']:
                start = i['start']
                end = i['end']
                curDates = splitToDays(start, end)
                for date in curDates:
                    if date >= startDate:
                        if date >= endDate:
                            break
                        hashDate = int((date - startDate)/DAY) + 1
                        name = str(id) + "-" + str(date)
                        graph.add_node(name,id=df.loc[index]['id'],price=df.loc[index]['price']['nightly'],date=date)
                        hashtable[hashDate].append(name)

def graphMultithreadingHelper2(hashtable, graph, startIndex, endIndex):
    for i in range(startIndex, endIndex):
        for first in hashtable[i]:
            for scnd in hashtable[i+1]:
                w = graph.node[scnd]['price']
                graph.add_edge(first,scnd,weight=w)

def splitToDays(start, end):
    dates = []
    start = toBaseDate(start)
    end = toBaseDate(end)
    while start <= end:
        dates.append(start)
        start += DAY
    return dates

def toBaseDate(unix):
    return unix - (unix%DAY)

def printResultPath(result, myGraph):
    lastID = 0
    startDate = 0
    price = 0
    cost = 0
    stops = []
    curDate = 0
    for day in (range(1, len(result))):
        listing = myGraph.node[result[day]]
        if lastID != listing['id']:
            newDate = listing['date']
            newID = listing['id']
            if(lastID!=0):
                stops.append("from " + printTime(startDate) + " to " + printTime(newDate) + ' in id: ' + str(lastID) + " price: " +str(price))
            lastID = newID
            startDate = newDate
            price = 0
        oldDate = curDate
        curDate = listing['date']
        days = (curDate - oldDate) / DAY
        if days != 1:
            addition = listing['priceweek']
        else:
            addition = listing['price']
        price += addition
        cost += addition
    for section in stops:
        print(section)
    print("total cost = " + str(cost))

def returnResultIds(results, graph):
    DAILY = 0
    WEEKLY = 1
    stops = []
    days = 0
    lastId = 0
    cost=0
    curId = 0
    startDate = 0
    price = [0,0]
    for node in range(1,len(results)):
        listing = graph.node[results[node]]
        if curId != listing['id']:
            if curId == 0:
                startDate = listing['date']
                price[DAILY] = listing['price']
                price[WEEKLY] = listing['priceweek']
                curId = listing['id']
            else:
                newDate = listing['date']
                days = int((newDate - startDate)/DAY)
                curPrice = (days//7)*price[WEEKLY] + (days%7)*price[DAILY]
                result = {'name':curId, 'price':curPrice, 'sdate':printTime(startDate), 'edate':printTime(newDate), 'days':days}
                stops.append(result)
                if listing['id'] != 0:
                    startDate = listing['date']
                    price[DAILY] = listing['price']
                    price[WEEKLY] = listing['priceweek']
                    curId = listing['id']
    return stops

def gbp_to_usd(gbp):
    rate = 1.4997
    return int(gbp * rate)
