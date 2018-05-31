# -*- coding: utf-8 -*-
"""
Created on Wed May  9 11:23:49 2018

@author: peipeiju
"""
#import numpy as np
#import time
from datetime import datetime, timedelta
#import datetime
import pandas as pd

txodata=pd.read_pickle("D:/ica/txo0301.pkl")
txdata=pd.read_pickle("D:/ica/tx0301.pkl")

#a = np.loadtxt('OWOSF_20170301.txt')

#with open('OWOSF_20170301.txt', 'r') as myfile:
#  data = myfile.readlines()

#file = open('data.txt', 'r')
#text = file.read().strip()
#file.close()

data=pd.read_table('OWOSF_20170301.txt',names = ["日期", "商品代號","買賣別","委託量","未成交量","委託價","委託方式","單種","開平倉碼","委託時間","委託序號","減量口數","交易與委託報價檔連結代碼"])
'''
dataMTF=pd.read_table('OWMTF_20170301.txt',names = ["日期", "商品代號","第一支腳商品代碼1","第一支腳買賣別1","第一支腳成交價格1","第一支腳成交數量1","第二支腳商品代碼2","第二支腳買賣別2","第二支腳成交價格2","第二支腳成交數量2","買賣別","成交價格","成交數量","開平倉碼","搓合標記","原始成交時間","單複式碼","交易與委託報價檔連結代碼"])
'''
u=data.loc[data['單種'] == 'U']
uu = u.reset_index(drop=True)
#只取txo部分
uu =uu.loc[uu['商品代號'].str[0:3]=='TXO']
uu = uu.reset_index(drop=True)

#只取有成交的
'''
ex_test = pd.merge(uu, dataMTF, on=["交易與委託報價檔連結代碼","買賣別"], how='inner')
ex_test = ex_test.drop(columns=['委託量','未成交量','委託方式','單種','開平倉碼_x','開平倉碼_y','委託序號','減量口數','日期_y','商品代號_y',"第一支腳商品代碼1","第一支腳買賣別1","第一支腳成交價格1","第一支腳成交數量1","第二支腳商品代碼2","第二支腳買賣別2","第二支腳成交價格2","第二支腳成交數量2",'搓合標記','單複式碼'])
ex_b = ex_test.loc[ex_test['買賣別'] == 'B']
ex_b = ex_b.reset_index(drop=True)
ex_s = ex_test.loc[ex_test['買賣別'] == 'S']
ex_s = ex_s.reset_index(drop=True)
'''
#太少了 放棄= =

#buy = uu[uu.index%1==0]
buy = uu.loc[uu['買賣別'] == 'B']
buy = buy.reset_index(drop=True)
sell = uu.loc[uu['買賣別'] == 'S']
sell = sell.reset_index(drop=True)

spread = sell['委託價']-buy['委託價']

t_s=pd.DataFrame()
#為了之後map方便 保留完整的商品代號
#t_s['商品代號']=buy['商品代號'].str[3:10]
t_s['商品類別']=buy['商品代號'].str[8:10]
t_s['履約價']=buy['商品代號'].str[3:8].astype(int)#履約價 轉成int之後才會把開頭的0去掉!!
#t_s['委託量buy']=buy['委託量']##########b s不一定一樣多???
#t_s['委託量sell']=sell['委託量']##########b s不一定一樣多???
#t_s['未成交量']###都是0??######待刪
t_s['委託價buy']=buy['委託價']#不能同時
t_s['委託價sell']=sell['委託價']#不能同時
t_s['Time']=buy['委託時間']
#t_s['減量口數buy']=buy['減量口數']
#t_s['減量口數sell']=sell['減量口數']
t_s['spread']=spread
#委託時間取到秒就好
t_s['Time']=t_s['Time'].str[0:8]
#創一個之後可以map的key
t_s['履約價']=t_s['履約價'].astype(str)#變回string方便串在一起
#t_s['key']=t_s['商品類別']+'_'+t_s['履約價']
t_s['key']=t_s['商品類別']+'_'+t_s['履約價']+'_'+t_s['Time']
#只取最窄的
t_s=t_s.loc[t_s.groupby('key').spread.idxmin()]
t_s = t_s.reset_index(drop=True)
###update
#改成merge前一秒的!!!因此t_s的Time要-1才會對到前一秒的testt
#t_s['Time']=datetime.strptime(t_s['Time'], "%H:%M:%S")
t_s['Time'] = pd.to_datetime(t_s['Time'], format="%H:%M:%S")
t_s['Time'] = t_s['Time']- timedelta(seconds=1)
t_s['Time'] = t_s['Time'].dt.strftime("%H:%M:%S")

###現在要多建共5秒的key
t_s['Time_2'] = pd.to_datetime(t_s['Time'], format="%H:%M:%S")
t_s['Time_2'] = t_s['Time_2']- timedelta(seconds=1)
t_s['Time_2'] = t_s['Time_2'].dt.strftime("%H:%M:%S")

t_s['Time_3'] = pd.to_datetime(t_s['Time'], format="%H:%M:%S")
t_s['Time_3'] = t_s['Time_3']- timedelta(seconds=2)
t_s['Time_3'] = t_s['Time_3'].dt.strftime("%H:%M:%S")

t_s['Time_4'] = pd.to_datetime(t_s['Time'], format="%H:%M:%S")
t_s['Time_4'] = t_s['Time_4']- timedelta(seconds=3)
t_s['Time_4'] = t_s['Time_4'].dt.strftime("%H:%M:%S")

t_s['Time_5'] = pd.to_datetime(t_s['Time'], format="%H:%M:%S")
t_s['Time_5'] = t_s['Time_5']- timedelta(seconds=4)
t_s['Time_5'] = t_s['Time_5'].dt.strftime("%H:%M:%S")

#建成要對上txo tx的key
#updated key
t_s['key']=t_s['商品類別']+'_'+t_s['履約價']+'_'+t_s['Time']
t_s['key2']=t_s['商品類別']+'_'+t_s['履約價']+'_'+t_s['Time_2']
t_s['key3']=t_s['商品類別']+'_'+t_s['履約價']+'_'+t_s['Time_3']
t_s['key4']=t_s['商品類別']+'_'+t_s['履約價']+'_'+t_s['Time_4']
t_s['key5']=t_s['商品類別']+'_'+t_s['履約價']+'_'+t_s['Time_5']

#在txodata也創key
#商品代號轉換
testt = txodata
testt['履約日期']=testt.index
testt = testt.reset_index(drop=True)
temp = pd.DataFrame(testt['履約日期'].tolist())

temp2=pd.DataFrame()
temp2['履約日期']=temp[1]
temp2['履約日期']=temp2['履約日期'].astype(str)+testt['Symbol']
temp2['年分']=temp2['履約日期'].str[3]
temp2['履約代號']=temp2['履約日期'].str[4:7]
temp2=temp2.replace({'01C':'A','02C':'B','03C':'C','04C':'D','05C':'E','06C':'F','07C':'G','08C':'H','09C':'I','10C':'J','11C':'K','12C':'L'})#字典映射  
temp2=temp2.replace({'01P':'M','02P':'N','03P':'O','04P':'P','05P':'Q','06P':'R','07P':'S','08P':'T','09P':'U','10P':'V','11P':'W','12P':'X'})#字典映射  
temp2['商品類別']=temp2['履約代號']+temp2['年分']
#testt = testt.rename(columns={'Contract':'履約價'})
testt['Contract']=testt['Contract'].astype(str)
#testt['key']=temp2['商品類別']+'_'+testt['Contract']
testt['key']=temp2['商品類別']+'_'+testt['Contract']+'_'+testt['Time']
###updated!!! txo low 裡面有不合理的值 因為沒有交易的時候他會設成100000
#理論上low最大不可能超過high 所以low裡面超過max(testt['High'].max()的都變成0)
#testt.loc[testt['Low']>testt['High'].max()]['Low']=0
testt.loc[(testt['Low']>10000),'Low']=0###########################################
#result_test = pd.merge(t_s, testt, on=['key', 'Time'], how='left')
result_test = pd.merge(t_s, testt, on=['key'], how='left')

#merge完之後有些對不上(可能秒數或什麼)
result_test = result_test.dropna(axis=0)#刪掉有na的row
result_test = result_test.reset_index(drop=True)

#整理一下把不要的column丟掉
#現在有兩個time 留一個就好
result_test = result_test.drop(columns=['履約日期','Contract','Date','Time_y'])
#統一RENAME
result_test = result_test.rename(columns={'Open':'Open_txo-1', 'High':'High_txo-1', 'Low':'Low_txo-1','Close':'Close_txo-1','Volume':'Volume_txo-1','Time_x':'Time'})

######用力merge5次
result_test = pd.merge(result_test, testt[['key','Open','High','Low','Close','Volume']], how='left', left_on=['key2'], right_on=['key'])
result_test = result_test.rename(columns={'Open':'Open_txo-2', 'High':'High_txo-2', 'Low':'Low_txo-2','Close':'Close_txo-2','Volume':'Volume_txo-2'})
result_test = pd.merge(result_test, testt[['key','Open','High','Low','Close','Volume']], how='left', left_on=['key3'], right_on=['key'])
result_test = result_test.rename(columns={'Open':'Open_txo-3', 'High':'High_txo-3', 'Low':'Low_txo-3','Close':'Close_txo-3','Volume':'Volume_txo-3'})
result_test = pd.merge(result_test, testt[['key','Open','High','Low','Close','Volume']], how='left', left_on=['key4'], right_on=['key'])
result_test = result_test.rename(columns={'Open':'Open_txo-4', 'High':'High_txo-4', 'Low':'Low_txo-4','Close':'Close_txo-4','Volume':'Volume_txo-4'})
result_test = pd.merge(result_test, testt[['key','Open','High','Low','Close','Volume']], how='left', left_on=['key5'], right_on=['key'])
result_test = result_test.rename(columns={'Open':'Open_txo-5', 'High':'High_txo-5', 'Low':'Low_txo-5','Close':'Close_txo-5','Volume':'Volume_txo-5'})
result_test = result_test.dropna(axis=0)#刪掉有na的row
result_test = result_test.reset_index(drop=True)

#抓tx資料
#只要留針對同一個時期的價格
#挑近月的 因為都取3月1日的所以都是201703到期的那一個
txtest = txdata.loc[txdata['Contract']=='201703']
#留需要的column就好
txtest = txtest.drop(columns=['Symbol','Contract','Date'])
#merge
result_test = pd.merge(result_test, txtest, on=['Time'], how='left')
#merge完之後有些對不上(可能秒數或什麼) 重新整理一下
result_test = result_test.dropna(axis=0)#刪掉有na的row
result_test = result_test.reset_index(drop=True)
#rename
result_test = result_test.rename(columns={'Open':'Open_tx-1', 'High':'High_tx-1', 'Low':'Low_tx-1','Close':'Close_tx-1','Volume':'Volume_tx-1'})

######用力merge5次
result_test = pd.merge(result_test, txtest[['Time','Open','High','Low','Close','Volume']], how='left', left_on=['Time_2'], right_on=['Time'])
result_test = result_test.rename(columns={'Open':'Open_tx-2', 'High':'High_tx-2', 'Low':'Low_tx-2','Close':'Close_tx-2','Volume':'Volume_tx-2'})
result_test = pd.merge(result_test, txtest[['Time','Open','High','Low','Close','Volume']], how='left', left_on=['Time_3'], right_on=['Time'])
result_test = result_test.rename(columns={'Open':'Open_tx-3', 'High':'High_tx-3', 'Low':'Low_tx-3','Close':'Close_tx-3','Volume':'Volume_tx-3'})
result_test = pd.merge(result_test, txtest[['Time','Open','High','Low','Close','Volume']], how='left', left_on=['Time_4'], right_on=['Time'])
result_test = result_test.rename(columns={'Open':'Open_tx-4', 'High':'High_tx-4', 'Low':'Low_tx-4','Close':'Close_tx-4','Volume':'Volume_tx-4'})
result_test = pd.merge(result_test, txtest[['Time','Open','High','Low','Close','Volume']], how='left', left_on=['Time_5'], right_on=['Time'])
result_test = result_test.rename(columns={'Open':'Open_tx-5', 'High':'High_tx-5', 'Low':'Low_tx-5','Close':'Close_tx-5','Volume':'Volume_tx-5'})
#merge完之後有些對不上(可能秒數或什麼) 重新整理一下
result_test = result_test.dropna(axis=0)#刪掉有na的row
result_test = result_test.reset_index(drop=True)


#result_test.to_pickle("D:/ica/0301data-1.pkl")#期交所台指期秒資料

#加一個feature 距離履約還有幾秒
temp_t=pd.DataFrame()
#strike_time = datetime.strptime("2017/03/1513:45:00", "%Y/%m/%d%H:%M:%S")####錯啦
#等等!!!!我的履約日期並非都是3月
#依照每個商品代號推算日期
temp_t['商品類別']=result_test['商品類別']
temp_t=temp_t.replace({'A7':'2017/01/18','B7':'2017/02/15','C7':'2017/03/15','D7':'2017/04/19','E7':'2017/05/17','F7':'2017/06/21','G7':'2017/07/19','H7':'2017/08/16','I7':'2017/09/20','J7':'2017/10/18','K7':'2017/11/15','L7':'2017/12/20'})#字典映射  
temp_t=temp_t.replace({'M7':'2017/01/18','N7':'2017/02/15','O7':'2017/03/15','P7':'2017/04/19','Q7':'2017/05/17','R7':'2017/06/21','S7':'2017/07/19','T7':'2017/08/16','U7':'2017/09/20','V7':'2017/10/18','W7':'2017/11/15','X7':'2017/12/20'})#字典映射  
temp_t['商品類別']= pd.to_datetime(temp_t['商品類別']+"13:45:00", format="%Y/%m/%d%H:%M:%S")

temp_t['Time'] = pd.to_datetime("2017/03/01"+result_test['Time'], format="%Y/%m/%d%H:%M:%S")
#seconds = (strike_time-temp_t['Time']).dt.seconds
temp_t['Time_due'] = (temp_t['商品類別']-temp_t['Time']).dt.total_seconds()
result_test['Due_Seconds'] = temp_t['Time_due']

result_test.to_pickle("D:/ica/0301data_se-5.pkl")#期交所台指期秒資料
#發現1 差價是40的時候委託量 都=12 因此可以去掉差價=40的部分
#發現2 差價是25的時候委託量 都=10or12 因此可以去掉差價=25的部分
#發現3 差價是20的時候委託量 都=20 只有一個=12 因此可以去掉差價=20的部分 
'''
t_s_new=t_s[t_s['差價']!=40]
t_s_new=t_s_new[t_s_new['差價']!=25]
t_s_new=t_s_new[t_s_new['差價']!=20]
'''
#先依據委託量分類 委託量分幾個類別>?