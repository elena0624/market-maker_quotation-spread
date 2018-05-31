# -*- coding: utf-8 -*-
"""
Created on Thu May 17 17:14:54 2018

@author: peipeiju
"""
import pandas as pd
import numpy as np
#result_test=pd.read_pickle("D:/ica/0301data.pkl")
result_test=pd.read_pickle("D:/ica/0301data_se-1.pkl")
#為啥low txo有怪怪的值????1e+5哪來的????
#先將每個商品分開
set(result_test['商品類別'])
#共有10種商品

#最簡單的網路=>每個商品分開 feature=當秒tx txo的開 履約價 委託量(buy) 委託量(sell) 委託價(???) 不管time 
#不館減量口數....
#result_test=result_test.dropna(axis=0)#刪掉有na的row
#result_test = result_test.reset_index(drop=True)
#C7_data = result_test.loc[result_test['商品類別']=='C7']
#C7_data = result_test.loc[result_test['商品類別']=='O7']
#C7_data = result_test.loc[result_test['Symbol']=='C']
#C7_data = result_test.loc[result_test['履約價']=='9800']
C7_data = result_test
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
C7_data['Open_tx-1'] = C7_data['Open_tx-1'].astype(float)/10000#ex.可以改成當秒的平均or拿開盤當1 優化normalized方式
#C7_data['Open_tx-1'] = (C7_data['Open_tx-1'].astype(float)-9500)/500
C7_data['High_tx-1'] = C7_data['High_tx-1'].astype(float)/10000
#C7_data['High_tx-1'] = (C7_data['High_tx-1'].astype(float)-9500)/500
C7_data['Low_tx-1'] = C7_data['Low_tx-1'].astype(float)/10000
#C7_data['Low_tx-1'] = (C7_data['Low_tx-1'].astype(float)-9500)/500
C7_data['Close_tx-1'] = C7_data['Close_tx-1'].astype(float)/10000
#C7_data['Close_tx-1'] = (C7_data['Close_tx-1'].astype(float)-9500)/500
C7_data['Volume_tx-1'] = C7_data['Volume_tx-1'].astype(float)/1500#找個有意義的值 應該是int??
C7_data['委託價buy'] = C7_data['委託價buy'].astype(float)/1000#找個有意義的值
C7_data['中價'] = C7_data['中價'].astype(float)/1000#找############
C7_data['spread'] = C7_data['spread'].astype(float)/20
#######
#C7_data['Due_Seconds'] = (C7_data['Due_Seconds'].astype(float)-1209500)/18000########test C7的時候用
C7_data['Due_Seconds'] = (C7_data['Due_Seconds'].astype(float)-1209500)/17000000########test C的時候用

C7_data = C7_data.sample(frac=1, random_state=7).reset_index(drop=True)

C7_train = C7_data[0:200000]
#C7_train = C7_data[0:45000]#怎麼少這麼1多!!!因為現在只取最窄的
C7_test = C7_data[200000:]
#C7_test = C7_data[45000:]
#C7_train_x = C7_train[['履約價', 'Open_txo-1','High_txo-1','Low_txo-1','Close_txo-1','Volume_txo-1',
#                       'Open_tx-1','High_tx-1','Low_tx-1','Close_tx-1','Volume_tx-1','委託價buy','Due_Seconds']]
C7_train_x = C7_train[['履約價', 'Open_txo-1','High_txo-1','Low_txo-1','Close_txo-1','Volume_txo-1',
                       'Open_tx-1','High_tx-1','Low_tx-1','Close_tx-1','Volume_tx-1','Due_Seconds','中價']]

C7_train_y = C7_train[['spread']]
#C7_test_x = C7_test[['履約價', 'Open_txo-1','High_txo-1','Low_txo-1','Close_txo-1','Volume_txo-1',
#                       'Open_tx-1','High_tx-1','Low_tx-1','Close_tx-1','Volume_tx-1','委託價buy','Due_Seconds']]
C7_test_x = C7_test[['履約價', 'Open_txo-1','High_txo-1','Low_txo-1','Close_txo-1','Volume_txo-1',
                       'Open_tx-1','High_tx-1','Low_tx-1','Close_tx-1','Volume_tx-1','Due_Seconds','中價']]
C7_test_y = C7_test[['spread']]

#建網路
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
#from sklearn.decomposition import PCA
from keras.models import Sequential
from keras.layers import Dense, Activation
import matplotlib.pyplot as plt
model = Sequential([
    Dense(20, input_shape=(13,)),
    Activation('relu'),
    Dense(15),
    Activation('relu'),
    Dense(10),
    Activation('relu'),
    Dense(1),
     Activation('sigmoid'),
#    Activation('sigmoid'),
])

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

bid_p=C7_train_x['中價']+(pred_C7_train_y/2).flatten()
ask_p=C7_train_x['中價']-(pred_C7_train_y/2).flatten()
plt.plot(bid_p[0:100])
plt.plot(C7_train_x['中價'][0:100])
plt.plot(ask_p[0:100])

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