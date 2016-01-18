from userLikes import sendPredicts,sendTrainingSet
import webbrowser
from time import sleep

array = sendTrainingSet()
for i in range(len(array)):
    sleep(1)
    webbrowser.open_new(str(array[i][0]))
#SeanUserLikes = [0,0,0,1,1,0,1,0,0,1,1,0,1,0,0,0,1,0,0,1]
#BenUserLikes = [0,1,0,0,0,1,1,0,0,0,1,1,0,0,0,1,0,1,0,1]
#GuyuserLikes = [0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0]
#DannyuserLikes = [0,0,1,0,1,0,1,0,0,0,1,0,0,1,0,1,0,1,1,1]
#ErezuserLikes = [0,1,1,0,1,1,0,1,1,1,1,0,1,1,0,1,0,1,0,1]
#predicts = sendPredicts(userLikes)
#for j in range(len(predicts)):
#    webbrowser.open_new(str(predicts[j][0]))