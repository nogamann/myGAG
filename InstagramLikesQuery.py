from instagram.client import InstagramAPI

access_token = "25290587.1677ed0.7131ff8507da447bb7fe54dab79fd273"
client_secret = "a8545940747f4536873f06e4a60c23a4"
api = InstagramAPI(access_token=access_token, client_secret=client_secret)
recent_media, next_ = api.user_recent_media(user_id="259220806", count=1)

for media in recent_media:
   print (media.caption.text)
   curMedia = str(media)
   curMedia = curMedia[7:]
   likesArr = api.media_likes(curMedia)
   print (likesArr)

followersList = open('followersList.txt', 'w+')
followers, next = api.user_followed_by(user_id="259220806")
count = 0
while len(followers)<100:
    more_follows, next = api.user_followed_by(with_next_url=next)
    followers.extend(more_follows)
    count += 50
#strFollowers = []
#for name in followers:
#   strFollowers.append(str(name)[6:])
for name in followers:
   curMedia = api.user_liked_media()
#user = api.user()
