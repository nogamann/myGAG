def createArr(usersHashMap,numberOfNeighbors):
    index = 0
    usersArr = [0]*numberOfNeighbors
    usersVectorsArr = [0]*numberOfNeighbors
    for key in usersHashMap:
        usersArr[index] = [index,key,usersHashMap[key]]
        usersVectorsArr[index] = usersHashMap[key]
        index += 1
    return usersVectorsArr,usersArr