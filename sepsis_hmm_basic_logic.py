# -*- coding: utf-8 -*-
"""sih2020.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18UD8zUXHM2RDEXN8v6Lf2Zq2Q-dFBB6G
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
# % matplotlib inline
sns.set_style("whitegrid") 
import warnings
warnings.filterwarnings("ignore")

x=pd.read_csv("ntrain1.csv")

y=pd.read_csv("test_patient.csv")

x.head()

x.describe()

print(x.keys())
print(y.keys())

def null_values(x,y):
  print("Training data:(total no of null values)")
  print(pd.isnull(x).sum())
  print("  ")
  print("Test data:(total no of null values)")
  print(pd.isnull(y).sum())
  
null_values(x,y)

print(x.keys())

x.drop(x.columns[[9,11,12,13,14,15,16,17,18,20,23,24,25,27,28,29,30,32,36,37,39]], axis = 1, inplace = True) 
#x.drop(x.columns[23:31], axis = 1, inplace = True)
y.drop(y.columns[[9,11,12,13,14,15,16,17,18,20,23,24,25,27,28,29,30,32,36,37,39]], axis = 1, inplace = True) 
#y.drop(y.columns[23:31], axis = 1, inplace = True)
null_values(x,y)

copy=x.copy()
#copy.dropna(inplace=True)
sns.distplot(copy["Age"])

#nba["College"].fillna("No College", inplace = True) 

#inplace of NaN values we will put median value
x[:].fillna(0,inplace = True)
y[:].fillna(0,inplace = True)
#x.head()
null_values(x,y)

#PLOTTING AND VISUALIZING DATA
#temporarily ignoring test data set
sns.barplot(x="Temp",y="SepsisLabel",data=x)
plt.title("Distribution of sepsis based on temp")
plt.show()

def stage1(temp1,hr1,resp1,wbc1,map1):
  flag1=0
  if(temp1<36 or temp>38):
    flag1=flag1+1
  if(hr1>90):
    flag1=flag1+1
  if(resp1>20):
    flag1=flag1+1
  if(wbc1<4 or wbc1>12):
    flag1=flag1+1

  if(flag1>=2):
    return 1
  else:
    return 0

def sofadetect(fio2,map2,bili2,plat2,sbp2,resp2,creat2):
  sofa1=0
  sofa2=0
  sofa3=0
  sofa4=0
  sofa5=0
  qsofa=0

  if(fio2>=0.4):
    sofa1=0
  elif(fio2<0.4 and fio2>0.3):
    sofa1=1
  elif(fio2<0.3 and fio2>0.2):
    sofa1=2
  elif(fio2<0.2 and fio2>0.1):
    sofa1=3
  elif(fio2<0.1):
    sofa1=4

  if(map2>=70):
    sofa2=0
  else:
    sofa2=1

  if(map2>=70):
    sofa2=0
  else:
    sofa2=1

  if(bili2<1.2):
    sofa3=0
  elif(bili2>=1.2 and bili2<=1.9):
    sofa3=1
  elif(bili2>=2 and bili2<=5.9):
    sofa3=2
  elif(bili2>=6 and bili2<=11.9):
    sofa3=3
  else:
    sofa3=4


  if(plat2>=150):
    sofa4=0
  elif(plat2<150 and plat2>=100):
    sofa4=1
  elif(plat2<100 and plat2>=50):
    sofa4=2
  elif(plat2<50 and plat2>=20):
    sofa4=3
  else:
    sofa4=4

  if(creat2<1.2):
    sofa5=0
  elif(creat2>=1.2 and creat2<=1.9):
    sofa5=1
  elif(creat2>=2 and creat2<=3.4):
    sofa5=2
  elif(creat2>=3.5 and creat2<=4.9):
    sofa5=3
  else:
    sofa5=4

  if(sbp2<=100):
    qsofa=1

  if(resp2>=22):
    qsofa=1

  return(sofa1,sofa2,sofa3,sofa4,sofa5,qsofa)

def stage2(fio2,map1,bili1,plat1,sbp1,resp1,creat1,temp1,hr1,wbc1,lact1):
  if(stage1(temp1,hr1,resp1,wbc1,map1)==1):
    sf1,sf2,sf3,sf4,sf5,qsf=sofadetect(fio2,map1,bili1,plat1,sbp1,resp1,creat1)
    if((sf1>=2 or sf2>=2 or sf3>=2 or sf4>=2 or sf5>=2 or qsf==1) and sbp1<90 and lact1>4):
      print("Start monitoring for 6 hrs!!!")
      return 1
      
    else :
      return 0

print(x.keys())

#sns.pairplot(x)

print(x.keys())

#df = pd.read_csv('ntrain1.csv', delimiter='\t')
# this line creates a new column, which is a Pandas series.
new_column = 0
# we then add the series to the dataframe, which holds our parsed CSV file
x['SepsisStage'] = new_column
# save the dataframe to CSV
#df.to_csv('ntrain1.csv', sep='\t')

print(x.keys())

x.head()

#import csv
#with open('ntrain1.csv') as data_csv:
#   data = list(csv.reader(data_csv,delimiter='\t'))
#    
#   for line in data[0:5]:
#       print(line)

#data=x.iloc[:,:]
#tempdf=x.iloc[:,:]
for i in range(0,374):
  ans=0
  data=x.iloc[i:i+1,:]
  sepslab=int(data["SepsisLabel"])
  temp=int(data["Temp"])
  hr=int(data["HR"])
  resp=int(data["Resp"])
  wbc=int(data["WBC"])
  mp=int(data["MAP"])
  fio2=int(data["FiO2"])
  bili=int(data["Bilirubin_total"])
  plat=int(data["Platelets"])
  sbp=int(data["SBP"])
  creat=int(data["Creatinine"])
  lact=int(data["Lactate"])
  
  if(sepslab==1):
    s1result=stage1(temp,hr,resp,wbc,mp)
    if(s1result==1):
      ans=1

    s2result=stage2(fio2,mp,bili,plat,sbp,resp,creat,temp,hr,wbc,lact)
    if(s2result==1):
      ans=2
  #tempdf.iloc[i,:] = data.loc[:]
  x.iloc[i:i+1,22:23]=ans

  #x=data
  #print(type(data))
  print(data)
print(x.iloc[0:11,:])

  #
  #x.to_csv('ntrain1.csv')

# anstrfun=transfun(2,1)
# print(anstrfun)

print(x.keys())

def transfun(c1,c2):
  print(c1,c2)
  count1=0
  count2=0
  d2=x.iloc[1:2,:]
  d2sepsstage=int(d2["SepsisStage"])
  print(d2sepsstage)
  #d2=(x.iloc[0:1,43:44])
  if(d2sepsstage==c2):
    count2=count2+1
  for i in range(0,100):
    d1=x.iloc[i:i+1,:]
    d1sepsstage=int(d1["SepsisStage"])
    d2=x.iloc[i+1:i+2,:]
    d2sepsstage=int(d2["SepsisStage"])
    if(d2sepsstage==c2):
      count2=count2+1
      if(d1sepsstage==c1):
        count1=count1+1
  print(type(count1))
  print(type(count2))
  prob=0
  if(count2!=0):
    prob=float(count1/count2)

  return prob

anstrfun=transfun(1,2)
print(anstrfun)

arr = [[0 for i in range(3)] for j in range(3)]
for i in range(0,3):
  for j in range(0,3):
    arr[i][j]=transfun(i,j)

print(arr)

train_copy = x.groupby('Patient_id').mean().fillna(x.mean())
train_copy['SepsisLabel'][train_copy['SepsisLabel']!=0] = 1
x_nb = train_copy.drop(['SepsisLabel'],axis = 1)
y_nb = train_copy['SepsisLabel']

# store the feature matrix (X) and response vector (y) 
X = x_nb
y = y_nb 
  
# splitting X and y into training and testing sets 
from sklearn.model_selection import train_test_split 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1) 
  
# training the model on training set 
from sklearn.naive_bayes import GaussianNB 
gnb = GaussianNB() 
gnb.fit(X_train, y_train) 
  
# making predictions on the testing set 
y_pred = gnb.predict(X_test) 
  
# comparing actual response values (y_test) with predicted response values (y_pred) 
from sklearn import metrics 
print("Gaussian Naive Bayes model accuracy(in %):", metrics.accuracy_score(y_test, y_pred)*100)

hidden_states = ['stage1', 'stage2','stage3']
pi = [0.6, 0.3,0.1]
state_space = pd.Series(pi, index=hidden_states, name='stages')
print(state_space)
print('\n', state_space.sum())

a_df = pd.DataFrame(columns=hidden_states, index=hidden_states)
a_df.loc[hidden_states[0]] =transproblist[0]
a_df.loc[hidden_states[1]] =transproblist[1]
a_df.loc[hidden_states[2]] =transproblist[2]


print(a_df)

a = a_df.values
print('\n', a, a.shape, '\n')
print(a_df.sum(axis=1))

from pprint import pprint 

# create a function that maps transition probability dataframe 
# to markov edges and weights

def _get_markov_edges(Q):
    edges = {}
    for col in Q.columns:
        for idx in Q.index:
            edges[(idx,col)] = Q.loc[idx,col]
    return edges

edges_wts = _get_markov_edges(a_df)
pprint(edges_wts)

G = nx.MultiDiGraph()

# nodes correspond to states
G.add_nodes_from(states)
print(f'Nodes:\n{G.nodes()}\n')

# edges represent transition probabilities
for k, v in edges_wts.items():
    tmp_origin, tmp_destination = k[0], k[1]
    G.add_edge(tmp_origin, tmp_destination, weight=v, label=v)
print(f'Edges:')
pprint(G.edges(data=True))    

pos = nx.drawing.nx_pydot.graphviz_layout(G, prog='dot')
nx.draw_networkx(G, pos)

# create edge labels for jupyter plot but is not necessary
edge_labels = {(n1,n2):d['label'] for n1,n2,d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G , pos, edge_labels=edge_labels)
nx.drawing.nx_pydot.write_dot(G, 'pet_dog_markov.dot')

x.to_csv('newtrain.csv')

ycheck=pd.read_csv("newtrain.csv")
ycheck.head()

