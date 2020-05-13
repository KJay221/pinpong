import pickle

file=open('save/KNN_training_result.pickle','rb')
x=pickle.load(file)
print(x)

##for i in range(len(x)):
  ##print(x[i]["frame"])