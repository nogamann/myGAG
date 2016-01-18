__author__ = 'Erez Levanon'

import urllib.parse
import urllib.request
import json
import pandas as pd
from sys import argv
MAX_RESULTS = 12000
RADIUS = '25'

def buildDB(lat = '40.758895', long = '-73.9829423',dbName = "./static/data/temp.p"):

    moreResults = 1

    count = 0
    page = 1

    url = 'https://zilyo.p.mashape.com/search'
    xmashkey = 'bFjnXwZZp5msh3AIkSIt8PDpsny3p18fuWtjsnDVIL0eN8gh27'
    accept = 'application/json'
    headers = { 'X-Mashape-Key' : xmashkey , 'Accept' : accept}
    values = {'latitude' : str(lat),
              'longitude' : str(long),
              'maxdistance':RADIUS,
              'page':str(page),
              'resultsperpage':'50',
              'provider': 'airbnb'
              }

    data = urllib.parse.urlencode(values)
    url = url + "?" + data
    req = urllib.request.Request(url , headers=headers)
    with urllib.request.urlopen(req) as response:
        batch = json.loads(response.read().decode('utf-8'))
        df = pd.DataFrame(batch['result'])
    try:
        while moreResults != 0:
            page += 1

            url = 'https://zilyo.p.mashape.com/search'
            xmashkey = 'bFjnXwZZp5msh3AIkSIt8PDpsny3p18fuWtjsnDVIL0eN8gh27'
            accept = 'application/json'
            headers = {'X-Mashape-Key' : xmashkey , 'Accept' : accept}
            values = {'latitude' : str(lat),
              'longitude' : str(long),
              'maxdistance':'80',
              'page':str(page),
              'resultsperpage':'50',
              'provider': 'airbnb'
            }

            data = urllib.parse.urlencode(values)
            url = url + "?" + data
            req = urllib.request.Request(url , headers=headers)
            with urllib.request.urlopen(req) as response:
                if count>=MAX_RESULTS:
                    break
                batch = json.loads(response.read().decode('utf-8'))
                moreResults =  len(batch['result'])
                count+=moreResults
                print(count)
                df = pd.concat([df, pd.DataFrame(batch['result'])])
    finally:
        df.reset_index(inplace=1)
        print(df.info())
        print("saving big pickle")
        df.to_pickle(dbName)
        print("done saving big pickle")


def buildDbOnServer( lat = '40.758895', long = '-73.9829423'):

    moreResults = 1
    count = 0
    page = 1

    url = 'https://zilyo.p.mashape.com/search'
    xmashkey = 'bFjnXwZZp5msh3AIkSIt8PDpsny3p18fuWtjsnDVIL0eN8gh27'
    accept = 'application/json'
    headers = { 'X-Mashape-Key' : xmashkey , 'Accept' : accept}
    values = {'latitude' : str(lat),
              'longitude' : str(long),
              'maxdistance':RADIUS,
              'page':str(page),
              'resultsperpage':'50',
              'provider': 'airbnb'
              }

    data = urllib.parse.urlencode(values)
    url = url + "?" + data
    req = urllib.request.Request(url , headers=headers)
    with urllib.request.urlopen(req) as response:
        batch = json.loads(response.read().decode('utf-8'))
        df = pd.DataFrame(batch['result'])
    try:
        while moreResults != 0:
            page += 1

            url = 'https://zilyo.p.mashape.com/search'
            xmashkey = 'bFjnXwZZp5msh3AIkSIt8PDpsny3p18fuWtjsnDVIL0eN8gh27'
            accept = 'application/json'
            headers = { 'X-Mashape-Key' : xmashkey , 'Accept' : accept}
            values = {'latitude' : str(lat),
              'longitude' : str(long),
              'maxdistance':'80',
              'page':str(page),
              'resultsperpage':'50',
              'provider': 'airbnb'
            }

            data = urllib.parse.urlencode(values)
            url = url + "?" + data
            req = urllib.request.Request(url , headers=headers)
            with urllib.request.urlopen(req) as response:
                if count>=MAX_RESULTS:
                    break
                batch = json.loads(response.read().decode('utf-8'))
                moreResults = len(batch['result'])
                count += moreResults
                print(count)
                df = pd.concat([df, pd.DataFrame(batch['result'])])
    finally:
        df.reset_index(inplace=1)
        print(df.info())
        return df

def cleanDbFromPath(path, newPath):
    df = pd.DataFrame(pd.read_pickle(path))
    print('clearing db')
    toDelete = ['attr', 'priceRange', 'photos', 'location', 'provider', 'amenities', 'reviews', 'latLng', 'itemStatus']
    for i in toDelete:
        df.pop(i)
    print("done clearing db")
    print("saving small pickle")
    df.to_pickle(newPath)
    print("done saving small pickle")
    return df

def cleanDbFromDf(df, newPath):
    print('clearing db')
    toDelete = ['attr', 'priceRange', 'location', 'amenities', 'reviews', 'latLng', 'itemStatus']
    for i in toDelete:
        df.pop(i)
    print("done clearing db")
    print("saving small pickle")
    df.to_pickle(newPath)
    print("done saving small pickle")
    return df

def removeTooEarly(df, date):
    for j, row in df.iterrows():
        availability = row['availability']
        toPop = []
        for i in range(len(availability)):
            if row['availability'][i]['end'] < date:
                toPop.append(i)
        toPop.reverse()
        for k in toPop:
            availability.pop(k)
    return df

def removeTooLate(df, date):
    for j, row in df.iterrows():
        availability = row['availability']
        toPop = []
        for i in range(len(availability)):
            if row['availability'][i]['end'] > date:
                toPop.append(i)
        toPop.reverse()
        for k in toPop:
            availability.pop(k)
    return df


def clearNotAvailables(df):
    toPop = []
    for j, row in df.iterrows():
        availability = row['availability']
        if len(availability) == 0:
            toPop.append(j)
    df.drop(df.index[toPop],inplace=1)
    return df


def readPickle(path):
    return pd.DataFrame(pd.read_pickle(path))

if __name__ == '__main__':
    if len(argv) == 2:
        smallDb = argv[1]
    else:
        smallDb = './static/data/newNY_min.p'
    toSaveDf = buildDbOnServer()
    cleanDbFromDf(toSaveDf, smallDb)
