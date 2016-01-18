##--------------------------imports----------------------
from FacebookLikesQuery import getLikes
from usersHashMap import createHashMap
from findNnearest import findNearestNeighbors
from HashToArrays import createArr
from copy import copy, deepcopy
import numpy as np
from sklearn.neighbors import NearestNeighbors
import pickle
import facebook
import requests
import webbrowser
import json
import random

graph = facebook.GraphAPI(access_token='1010889892301604|0-CiTXs37lM2gOaoe9kO6eKLppQ', version='2.5')
##-------------------------main code---------------------
#create DataBase!!!
'''
PostLikeUsers, postIds = getLikes()


pickle.dump(postIds,open("postIds","wb"))
pickle.dump(PostLikeUsers,open("PostLikeUsers","wb"))

#Training Set - finding the nearset neighbors
'''
sizeOfTrainingSet = 20
postIds = pickle.load(open ("postIds","rb"))
PostLikeUsers = pickle.load(open ("PostLikeUsers","rb"))
arr = pickle.load(open ("arr","rb"))
indexes = pickle.load(open ("indexes","rb"))
print(indexes)
#randomIndex = list(random.sample(range(0,59),25))
usersHashMap = createHashMap(arr,sizeOfTrainingSet,indexes)
print(len(usersHashMap))
#usersHashMap = pickle.load(open ("usersHash","rb"))
#postIds = pickle.load(open ("postIds","rb"))
#PostLikeUsers = pickle.load(open ("PostLikeUsers","rb"))
numberOfPosts = len(postIds)
numberOfNeighbors = len(usersHashMap)

nearestNumber = 7
totalDiff = 0
usersVectorsArr,usersArr = createArr(usersHashMap,numberOfNeighbors)
tmpUsersVectorsArr = deepcopy(usersVectorsArr) #the full data on users
tmpUsersArr = deepcopy(usersArr) #only the likes array
#indexes = list(range(sizeOfTrainingSet))
fullUsersHashmap = pickle.load(open ("fullUsersHash","rb"))
print(len(fullUsersHashmap))

sample = list(random.sample(range(1,18315),5))
for numberOfTests in sample:
    tmpFullUsersHashmap = deepcopy(fullUsersHashmap)
    #print(numberOfTests)
    #test user
    userLikes = tmpUsersVectorsArr[numberOfTests]
    #print(userLikes)
    fullTestUser = tmpUsersArr[numberOfTests]
    #create temp arr without the test user
    tmpUsersVectorsArr.pop(numberOfTests)
    testArr = deepcopy(tmpUsersVectorsArr)
    tmpUsersArr.pop(numberOfTests)
    fullTestArr = deepcopy(tmpUsersArr)
    #find nearestNeighbors of the test user
    neighbors = findNearestNeighbors(userLikes, numberOfNeighbors-1,nearestNumber,testArr,fullTestArr)

    testUserLikes = tmpFullUsersHashmap[fullTestUser[1]]

#summing the average number of likes
    #i = 0
    #summing = 0
    #for key in newUsersHashMap:
    #    for like in newUsersHashMap[key]:
    #        summing += like
    #    if summing>4.5:
    #    i += summing
    #    summing = 0
    #print (i)
    #delete the testUser from the hashmap
    del tmpFullUsersHashmap[fullTestUser[1]]
    averages = [None]*numberOfPosts
    for j in range(numberOfPosts):
        average = 0
        for i in range(nearestNumber):
            neighbor = neighbors[i]
            average += tmpFullUsersHashmap[str(neighbor[1])][j]
        averages[j] = (average/nearestNumber)
    testLikes = [None]*numberOfPosts
    counter = 0
    for k in indexes:
        testLikes[k] = userLikes[counter]
        counter+=1
    #for id in postIds[sizeOfTrainingSet:]:
    for num in range(numberOfPosts):
        if num not in indexes:
            if (averages[num]>= 0.6):
                testLikes[num] = 1
            else:
                testLikes[num] = 0
    count = sum(1 for i, j in zip(testUserLikes, testLikes) if i != j)
    #summing = 0
    #for like in testUserLikes:
    #    summing = summing+like
    #if summing>=4.5:
    #   print("number of likes= " + str(summing))
    #    print("the number of differences= " +str(count))
    #    totalDiffOverAverage += count
    totalDiff = totalDiff + count
    tmpUsersVectorsArr = deepcopy(usersVectorsArr)
    tmpUsersArr = deepcopy(usersArr)
    tmpFullUsersHashmap = deepcopy(fullUsersHashmap)
    print(numberOfTests)
    #        image = requests.get("https://graph.facebook.com/"+str(id)+"?fields=full_picture")
    #        json_data = json.loads(image.text)
    #        picture = json_data['full_picture']
    #        webbrowser.open_new(picture)
    #    index += 1
print("the total diff are:"+str(totalDiff))

