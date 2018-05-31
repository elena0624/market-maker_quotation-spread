# -*- coding: utf-8 -*-
"""
Created on Thu May 17 17:14:54 2018

@author: peipeiju
"""
import pandas as pd
import numpy as np
#result_test=pd.read_pickle("D:/ica/0301data.pkl")
result_test=pd.read_pickle("D:/ica/0301data_se-5.pkl")
#為啥low txo有怪怪的值????1e+5哪來的????
#先將每個商品分開
set(result_test['商品類別'])
#共有10種商品

#最簡單的網路=>每個商品分開 feature=當秒tx txo的開 履約價 委託量(buy) 委託量(sell) 委託價(???) 不管time 
#不館減量口數....
#result_test=result_test.dropna(axis=0)#刪掉有na的row
#result_test = result_test.reset_index(drop=True)
#C7_data = result_test.loc[result_test['商品類別']=='C7']
#C7_data = result_test.loc[result_test['Symbol']=='P']
C7_data = result_test.loc[result_test['履約價']=='9800']
#C7_data = result_test
C7_data = C7_data.reset_index(drop=True)
#normalized 每一column 可以改成更有意義的除法
C7_data['履約價'] = C7_data['履約價'].astype(int)/10000
C7_data['中價'] = (C7_data['委託價sell'].astype(float) + C7_data['委託價buy'].astype(float))/2######
#C7_data['履約價'] = (C7_data['履約價'].astype(int)-6000)/6000#是6600~12000 優化normalized方式
#C7_data['委託量buy'] = C7_data['委託量buy'].astype(int)/200
#C7_data['委託量sell'] = C7_data['委託量sell'].astype(int)/200
C7_data['Open_txo-1'] = C7_data['Open_txo-1'].astype(float)/1000#ex.可以改成當秒的平均or拿開盤當1
C7_data['High_txo-1'] = C7_data['High_txo-1'].astype(float)/1000
C7_data['Low_txo-1'] = C7_data['Low_txo-1'].astype(float)/1000
C7_data['Close_txo-1'] = C7_data['Close_txo-1'].astype(float)/1000
C7_data['Volume_txo-1'] = C7_data['Volume_txo-1'].astype(float)/500###ex.平均交易量當1 應該是int?

C7_data['Open_txo-2'] = C7_data['Open_txo-2'].astype(float)/1000#ex.可以改成當秒的平均or拿開盤當1
C7_data['High_txo-2'] = C7_data['High_txo-2'].astype(float)/1000
C7_data['Low_txo-2'] = C7_data['Low_txo-2'].astype(float)/1000
C7_data['Close_txo-2'] = C7_data['Close_txo-2'].astype(float)/1000
C7_data['Volume_txo-2'] = C7_data['Volume_txo-2'].astype(float)/500###ex.平均交易量當1 應該是int?

C7_data['Open_txo-3'] = C7_data['Open_txo-3'].astype(float)/1000#ex.可以改成當秒的平均or拿開盤當1
C7_data['High_txo-3'] = C7_data['High_txo-3'].astype(float)/1000
C7_data['Low_txo-3'] = C7_data['Low_txo-3'].astype(float)/1000
C7_data['Close_txo-3'] = C7_data['Close_txo-3'].astype(float)/1000
C7_data['Volume_txo-3'] = C7_data['Volume_txo-3'].astype(float)/500###ex.平均交易量當1 應該是int?

C7_data['Open_txo-4'] = C7_data['Open_txo-4'].astype(float)/1000#ex.可以改成當秒的平均or拿開盤當1
C7_data['High_txo-4'] = C7_data['High_txo-4'].astype(float)/1000
C7_data['Low_txo-4'] = C7_data['Low_txo-4'].astype(float)/1000
C7_data['Close_txo-4'] = C7_data['Close_txo-4'].astype(float)/1000
C7_data['Volume_txo-4'] = C7_data['Volume_txo-4'].astype(float)/500###ex.平均交易量當1 應該是int?

C7_data['Open_txo-5'] = C7_data['Open_txo-5'].astype(float)/1000#ex.可以改成當秒的平均or拿開盤當1
C7_data['High_txo-5'] = C7_data['High_txo-5'].astype(float)/1000
C7_data['Low_txo-5'] = C7_data['Low_txo-5'].astype(float)/1000
C7_data['Close_txo-5'] = C7_data['Close_txo-5'].astype(float)/1000
C7_data['Volume_txo-5'] = C7_data['Volume_txo-5'].astype(float)/500###ex.平均交易量當1 應該是int?


C7_data['Open_tx-1'] = C7_data['Open_tx-1'].astype(float)/10000#ex.可以改成當秒的平均or拿開盤當1 優化normalized方式
C7_data['High_tx-1'] = C7_data['High_tx-1'].astype(float)/10000
C7_data['Low_tx-1'] = C7_data['Low_tx-1'].astype(float)/10000
C7_data['Close_tx-1'] = C7_data['Close_tx-1'].astype(float)/10000
C7_data['Volume_tx-1'] = C7_data['Volume_tx-1'].astype(float)/1500#找個有意義的值 應該是int??

C7_data['Open_tx-2'] = C7_data['Open_tx-2'].astype(float)/10000#ex.可以改成當秒的平均or拿開盤當1 優化normalized方式
C7_data['High_tx-2'] = C7_data['High_tx-2'].astype(float)/10000
C7_data['Low_tx-2'] = C7_data['Low_tx-2'].astype(float)/10000
C7_data['Close_tx-2'] = C7_data['Close_tx-2'].astype(float)/10000
C7_data['Volume_tx-2'] = C7_data['Volume_tx-2'].astype(float)/1500#找個有意義的值 應該是int??

C7_data['Open_tx-3'] = C7_data['Open_tx-3'].astype(float)/10000#ex.可以改成當秒的平均or拿開盤當1 優化normalized方式
C7_data['High_tx-3'] = C7_data['High_tx-3'].astype(float)/10000
C7_data['Low_tx-3'] = C7_data['Low_tx-3'].astype(float)/10000
C7_data['Close_tx-3'] = C7_data['Close_tx-3'].astype(float)/10000
C7_data['Volume_tx-3'] = C7_data['Volume_tx-3'].astype(float)/1500#找個有意義的值 應該是int??

C7_data['Open_tx-4'] = C7_data['Open_tx-4'].astype(float)/10000#ex.可以改成當秒的平均or拿開盤當1 優化normalized方式
C7_data['High_tx-4'] = C7_data['High_tx-4'].astype(float)/10000
C7_data['Low_tx-4'] = C7_data['Low_tx-4'].astype(float)/10000
C7_data['Close_tx-4'] = C7_data['Close_tx-4'].astype(float)/10000
C7_data['Volume_tx-4'] = C7_data['Volume_tx-4'].astype(float)/1500#找個有意義的值 應該是int??

C7_data['Open_tx-5'] = C7_data['Open_tx-5'].astype(float)/10000#ex.可以改成當秒的平均or拿開盤當1 優化normalized方式
C7_data['High_tx-5'] = C7_data['High_tx-5'].astype(float)/10000
C7_data['Low_tx-5'] = C7_data['Low_tx-5'].astype(float)/10000
C7_data['Close_tx-5'] = C7_data['Close_tx-5'].astype(float)/10000
C7_data['Volume_tx-5'] = C7_data['Volume_tx-5'].astype(float)/1500#找個有意義的值 應該是int??

C7_data['委託價buy'] = C7_data['委託價buy'].astype(float)/1000#找個有意義的值
C7_data['中價'] = C7_data['中價'].astype(float)/1000#找############
C7_data['spread'] = C7_data['spread'].astype(float)/20
#######
#C7_data['Due_Seconds'] = (C7_data['Due_Seconds'].astype(float)-1209500)/18000########test C7 O7的時候用
C7_data['Due_Seconds'] = (C7_data['Due_Seconds'].astype(float)-1209500)/17000000########test C的時候用
#C7_data['Due_Seconds'] = (C7_data['Due_Seconds'].astype(float)-4233600)/18000########test D7 P7的時候用
#C7_data['Due_Seconds'] = (C7_data['Due_Seconds'].astype(float)-6652000)/18000########test E7 Q7的時候用
#C7_data['Due_Seconds'] = (C7_data['Due_Seconds'].astype(float)-9676000)/18000########test F7 R7的時候用
#C7_data['Due_Seconds'] = (C7_data['Due_Seconds'].astype(float)-17539000)/18000########test I7 U7的時候用

C7_data = C7_data.sample(frac=1, random_state=7).reset_index(drop=True)

C7_train = C7_data[0:25000]
#C7_train = C7_data[0:4500]#怎麼少這麼1多!!!因為現在只取最窄的
#C7_train = C7_data[0:45000]
C7_test = C7_data[25000:]
#C7_test = C7_data[45000:]
#C7_test = C7_data[4500:]
C7_train_x = C7_train[['履約價', 'Open_txo-1','High_txo-1','Low_txo-1','Close_txo-1','Volume_txo-1',
                       'Open_tx-1','High_tx-1','Low_tx-1','Close_tx-1','Volume_tx-1','委託價buy','Due_Seconds',
                       'Open_txo-2','High_txo-2','Low_txo-2','Close_txo-2','Volume_txo-2',
                       'Open_tx-2','High_tx-2','Low_tx-2','Close_tx-2','Volume_tx-2',
                       'Open_txo-3','High_txo-3','Low_txo-3','Close_txo-3','Volume_txo-3',
                       'Open_tx-3','High_tx-3','Low_tx-3','Close_tx-3','Volume_tx-3',
                       'Open_txo-4','High_txo-4','Low_txo-4','Close_txo-4','Volume_txo-4',
                       'Open_tx-4','High_tx-4','Low_tx-4','Close_tx-4','Volume_tx-4',
                       'Open_txo-5','High_txo-5','Low_txo-5','Close_txo-5','Volume_txo-5',
                       'Open_tx-5','High_tx-5','Low_tx-5','Close_tx-5','Volume_tx-5']]
C7_train_y = C7_train[['spread']]
C7_test_x = C7_test[['履約價', 'Open_txo-1','High_txo-1','Low_txo-1','Close_txo-1','Volume_txo-1',
                       'Open_tx-1','High_tx-1','Low_tx-1','Close_tx-1','Volume_tx-1','委託價buy','Due_Seconds',
                       'Open_txo-2','High_txo-2','Low_txo-2','Close_txo-2','Volume_txo-2',
                       'Open_tx-2','High_tx-2','Low_tx-2','Close_tx-2','Volume_tx-2',
                       'Open_txo-3','High_txo-3','Low_txo-3','Close_txo-3','Volume_txo-3',
                       'Open_tx-3','High_tx-3','Low_tx-3','Close_tx-3','Volume_tx-3',
                       'Open_txo-4','High_txo-4','Low_txo-4','Close_txo-4','Volume_txo-4',
                       'Open_tx-4','High_tx-4','Low_tx-4','Close_tx-4','Volume_tx-4',
                       'Open_txo-5','High_txo-5','Low_txo-5','Close_txo-5','Volume_txo-5',
                       'Open_tx-5','High_tx-5','Low_tx-5','Close_tx-5','Volume_tx-5']]
C7_test_y = C7_test[['spread']]

#建網路
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
#from sklearn.decomposition import PCA
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
import matplotlib.pyplot as plt
model = Sequential([
    Dense(300, input_shape=(53,)),
    Activation('relu'),
    Dense(50),
    Activation('relu'),
#    Dropout(0.5),
    Dense(25),
    Activation('relu'),
    Dense(10),
    Activation('relu'),
    Dense(1),
     Activation('sigmoid'),
#    Activation('sigmoid'),
])
#model = Sequential()
#model.add(Dense(100, input_dim=53, kernel_initializer='normal', activation='relu'))
#model.add(Dropout(0.5))
#model.add(Dense(30, kernel_initializer='normal', activation='relu'))
#model.add(Dropout(0.2))
#model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))



model.compile(optimizer='adam', loss='mse')
history = model.fit(C7_train_x, C7_train_y, batch_size=256, validation_split=0.05, epochs=150)
#model.fit(train_X_normed, train_Y, validation_split = 0.1, epochs=200)
pred_C7_train_y = model.predict(C7_train_x)
pred_C7_test_y = model.predict(C7_test_x)
print("train:")
print( np.mean(np.abs((pred_C7_train_y-C7_train_y))) )
print("test:")
print(np.mean(np.abs((pred_C7_test_y-C7_test_y))) )
print("train percent:")
print( np.mean(np.abs((pred_C7_train_y-C7_train_y))/C7_train_y) )
print("test percent:")
print(np.mean(np.abs((pred_C7_test_y-C7_test_y))/C7_test_y) )

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()

C7_test_y= C7_test_y.reset_index(drop=True)
plt.plot(C7_test_y[0:100],label='truth')
plt.plot(pred_C7_test_y[0:100],label='predict')
#plt.title('spread/10')
plt.ylabel('spread/20')
plt.xlabel('#')
plt.legend()
plt.show()
#print(np.mean(np.abs((pred_Y_normed-test_Y))))
##print(np.mean(np.abs(pred_Y-test_Y)))
#print("亂猜 "+str(np.mean(np.abs((np.mean(train_Y)-test_Y)))))#test