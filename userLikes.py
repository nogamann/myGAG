import requests
import json
from mainNoDebug import predictLikes
import pickle

def sendPredicts(userLikes):
    postIds = pickle.load(open ("postIds","rb"))
    predicts = predictLikes(userLikes)
    posts = []
    for index in predicts:
        post = postIds[index]
        image = requests.get("https://graph.facebook.com/"+str(post)+"?fields=full_picture,message")
        json_data = json.loads(image.text)
        picture = json_data['full_picture']
        message = json_data['message']
        curPost = [picture,message]
        posts.append(curPost)
        print(index)
    return posts

def sendTrainingSet():
    posts = pickle.load(open ("firstPosts","rb"))
    #happens once
    #indexes = pickle.load(open ("indexes","rb"))
    #postIds = pickle.load(open ("postIds","rb"))
    #posts = []
    #for index in indexes:
    #    post = postIds[index]
    #    image = requests.get("https://graph.facebook.com/"+str(post)+"?fields=full_picture,message")
    #    json_data = json.loads(image.text)
    #    picture = json_data['full_picture']
    #    message = json_data['message']
    #    curPost = [picture,message]
    #    posts.append(curPost)
    #pickle.dump(posts,open("firstPosts","wb"))
    return(posts)