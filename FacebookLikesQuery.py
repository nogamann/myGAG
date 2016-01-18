import facebook
import json
import requests
from time import sleep

def getLikes():
    numberOfPosts = 200
    graph = facebook.GraphAPI(access_token='1010889892301604|0-CiTXs37lM2gOaoe9kO6eKLppQ', version='2.5')
    response = requests.get("https://graph.facebook.com/Memes.fr/feed?access_token=1010889892301604|0-CiTXs37lM2gOaoe9kO6eKLppQ")
    json_data = json.loads(response.text)
    PostLikeUsers = [[] for i in range(numberOfPosts)]
    postIds = []
    counter = 1
    #run over 100 posts
    while 'next' in json_data['paging'] and counter<numberOfPosts:
        #for each post from the last 20 posts
        for post in json_data['data']:
            curList = []
            print('We are in post number:'+str(counter))
            postIds.append(str(post['id']))
            #curPost = graph.get_object(str(post['id']))
            likes = graph.get_connections(id=str(post['id']), connection_name='likes')
            if (likes['data'] != []):
                for id in likes['data']:
                    curId = (id['id'])
                    curList.append(curId)
                #while there are more likes
                while ('next' in likes['paging']):
                    likes = requests.get(likes['paging']['next'])
                    likes = json.loads(likes.text)
                    if (('data' not in likes) or ('error' in likes)):
                        break
                    else:
                        for id in likes['data']:
                            curId = (id['id'])
                            curList.append(curId)
                PostLikeUsers[counter-1].append(curList)
            counter += 1
            if counter>numberOfPosts:
                break
        response = requests.get(json_data['paging']['next'])
        json_data = json.loads(response.text)
    return PostLikeUsers, postIds