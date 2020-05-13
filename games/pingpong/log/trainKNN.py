import pickle
import numpy as np
from os import path
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier

if __name__ == '__main__':  
  ball_x=np.array([])
  ball_y=np.array([])
  ball_speed_x=np.array([])
  ball_speed_y=np.array([])
  direction=np.array([])    ##1、2、3、4跟象限一樣
  platform_1P=np.array([])
  platform_2P=np.array([])
  blocker_x=np.array([])
  vector_x=np.array([])
  vector_y=np.array([])
  platform_1P_move=np.array([])
  platform_2P_move=np.array([])

  for i in range(1,15):
    file=open(str(i)+'.pickle','rb')
    data=pickle.load(file)
    vector_x=np.append(vector_x,0)
    vector_y=np.append(vector_y,0)
    for i in range(len(data)):
      ball_x=np.append(ball_x,data[i]["ball"][0])
      ball_y=np.append(ball_y,data[i]["ball"][1])
      ball_speed_x=np.append(ball_speed_x,data[i]["ball_speed"][0])
      ball_speed_y=np.append(ball_speed_y,data[i]["ball_speed"][1])
      platform_1P=np.append(platform_1P,data[i]["platform_1P"][0])
      platform_2P=np.append(platform_2P,data[i]["platform_2P"][0])
      blocker_x=np.append(blocker_x,data[i]["blocker"][0])

      if i>0:
        vector_x=np.append(vector_x,ball_x[i]-ball_x[i-1])
        vector_y=np.append(vector_y,ball_y[i]-ball_y[i-1])

      if ball_speed_x[i]>0 and ball_speed_y[i]>0:
        direction=np.append(direction,1)
      elif ball_speed_x[i]<0 and ball_speed_y[i]>0:
        direction=np.append(direction,2)
      elif ball_speed_x[i]<0 and ball_speed_y[i]<0:
        direction=np.append(direction,3)
      elif ball_speed_x[i]>0 and ball_speed_y[i]<0:
        direction=np.append(direction,4)
      else :
        direction=np.append(direction,0)

      if data[i]["command_1P"] == "MOVE_RIGHT" :
        platform_1P_move=np.append(platform_1P_move,5)
      elif data[i]["command_1P"]=="MOVE_LEFT":
        platform_1P_move=np.append(platform_1P_move,-5)
      else :
        platform_1P_move=np.append(platform_1P_move,0)

      if data[i]["command_2P"] == "MOVE_RIGHT" :
        platform_2P_move=np.append(platform_2P_move,5)
      elif data[i]["command_2P"]=="MOVE_LEFT":
        platform_2P_move=np.append(platform_2P_move,-5)
      else :
        platform_2P_move=np.append(platform_2P_move,0)

  train_data=np.vstack((platform_1P,vector_x,vector_y,ball_speed_x,ball_speed_y,platform_2P))
  train_data=np.rot90(train_data,-1)## platform2P speedy speedx  y x platform_1P
  target_data=platform_1P_move
  
  x_train , x_test , y_train , y_test = train_test_split(train_data,target_data,test_size=0.2)
  platform_predict_clf = KNeighborsClassifier(n_neighbors=3).fit(train_data,target_data)
  y_predict = platform_predict_clf.predict(x_test)
  print(y_predict)
  accuracy = metrics.accuracy_score(y_test, y_predict)
  print("Accuracy(正確率) ={:8.3f}%".format(accuracy*100))

  with open('save/KNN_training_result.pickle', 'wb') as f:
    pickle.dump(platform_predict_clf, f)
  
  
  
  
  
  

