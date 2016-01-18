import numpy as np
from sklearn.neighbors import NearestNeighbors
def findNearestNeighbors(userLikes,numberOfNeighbors,nearestNumber,usersVectorsArr,usersArr):
    neigh = NearestNeighbors(numberOfNeighbors)
    neigh.fit(usersVectorsArr)
    nearest = neigh.kneighbors([userLikes],nearestNumber,return_distance=False)
    arr = np.asarray(nearest[0])
    array = []
    for neighborCount in range(nearestNumber):
        array.append(usersArr[arr[neighborCount]])
    return array