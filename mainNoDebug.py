##--------------------------imports----------------------
# from FacebookLikesQuery import getLikes
# from usersHashMap import createHashMap
from findNnearest import findNearestNeighbors
from HashToArrays import createArr
# from copy import copy, deepcopy
# import numpy as np
# from sklearn.neighbors import NearestNeighbors
# from findIndexList import createIndexList
import pickle
import facebook
# import requests
# import webbrowser
# import json
# import random

# graph = facebook.GraphAPI(access_token='1010889892301604|0-CiTXs37lM2gOaoe9kO6eKLppQ', version='2.5')
'''
PostLikeUsers, postIds = getLikes()

pickle.dump(postIds,open("postIds","wb"))
pickle.dump(PostLikeUsers,open("PostLikeUsers","wb"))

postIds = pickle.load(open ("postIds","rb"))
PostLikeUsers = pickle.load(open ("PostLikeUsers","rb"))

numberOfPosts = len(postIds)

#create array of posts
arr=[]
for post in PostLikeUsers:
    for p in post:
        arr.append(p)
#create full hashmap
pickle.dump(arr,open("arr","wb"))

#createfullHahmap
postIds = pickle.load(open ("postIds","rb"))
numberOfPosts = len(postIds)
arr = pickle.load(open ("arr","rb"))
indexes = list(range(numberOfPosts))
fullUsersHashMap = createHashMap(arr,numberOfPosts,indexes)
pickle.dump(fullUsersHashMap,open("fullUsersHash","wb"))

#creating indexes
sizeOfTrainingSet = 20
arr = pickle.load(open ("arr","rb"))
indexes = createIndexList(arr,sizeOfTrainingSet)
pickle.dump(indexes,open("indexes","wb"))

#Training Set create indexed hashmap

#create IndexesHashmap once
arr = pickle.load(open ("arr","rb"))
sizeOfTrainingSet = 20
indexes = pickle.load(open ("indexes","rb"))
indexesHashMap = createHashMap(arr,sizeOfTrainingSet,indexes)
pickle.dump(indexesHashMap,open("indexesHashMap","wb"))
'''
def predictLikes(userLikes):
    postIds = pickle.load(open ("postIds","rb"))
    indexes = pickle.load(open ("indexes","rb"))
    numberOfPosts = len(postIds)
    indexesHashMap = pickle.load(open ("indexesHashMap","rb"))
    numberOfNeighbors = len(indexesHashMap)
    usersVectorsArr,usersArr = createArr(indexesHashMap,numberOfNeighbors)
    nearestNumber = 7
    neighbors = findNearestNeighbors(userLikes, numberOfNeighbors,nearestNumber,usersVectorsArr,usersArr)
    fullUsersHashMap = pickle.load(open ("fullUsersHash","rb"))
    averages = [None]*numberOfPosts
    for j in range(numberOfPosts):
        average = 0
        weight = nearestNumber
        for i in range(nearestNumber):
            neighbor = neighbors[i]
            average += fullUsersHashMap[str(neighbor[1])][j]*weight
            weight -= 1
        averages[j] = (average/28)
        #averages[j] = (average/nearestNumber)
    print(averages)
    testLikes = [None]*numberOfPosts
    counter = 0
    for i in indexes:
        testLikes[i] = userLikes[counter]
        counter += 1
    newIndexes =[]
    lastIndexes=[]
    filterNum = 0.0
    while (len(newIndexes)<6):
        filterNum += 0.1
        newIndexes = []
        for num in range(numberOfPosts):
            if num not in indexes:
                if (averages[num]>= (1-filterNum)):
                    newIndexes.append(num)
                    #testLikes[num] = 1
                #else:
                    #testLikes[num] = 0
    if len(newIndexes)>20:
        newIndexes = newIndexes[:20]
    print (filterNum)
    return newIndexes