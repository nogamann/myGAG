from copy import copy, deepcopy

def createIndexList(arr,size):
    tmpArr = deepcopy(arr)
    i=0
    for post in tmpArr:
        post.append(i)
        i+=1
    indexes = []
    while len(indexes)<size:
        sorted_arr = sorted(tmpArr,key=len,reverse=True)
        indexes.append(sorted_arr[0][-1])
        for post in sorted_arr:
            post = [x for x in post if x not in sorted_arr[0]]
        tmpArr = sorted_arr[1:]
    return indexes