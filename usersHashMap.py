from FacebookLikesQuery import getLikes
import pickle

def createHashMap(postLikes,sizeOfSet,indexes):
    "creating hash map that holds each user with the post ids he likes"
    usersHashMap = {}
    i = 0
    #numberOfLikes = 0
    for post in postLikes: #running over the users who liked the post
        if i in indexes:
            for user in post:
                #numberOfLikes += 1
                if user in usersHashMap:
                    curIndex = indexes.index(i)
                    usersHashMap[user][curIndex] = 1
                else:
                    usersHashMap[user] = [0] * sizeOfSet
                    curIndex = indexes.index(i)
                    usersHashMap[user][curIndex] = 1
        i += 1
    #print(numberOfLikes)
    return usersHashMap