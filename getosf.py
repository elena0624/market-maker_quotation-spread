# -*- coding: utf-8 -*-
"""
Created on Wed May  9 11:23:49 2018

@author: peipeiju
"""
from datetime import datetime, timedelta
import pandas as pd

txodata=pd.read_pickle("D:/ica/txo0301.pkl")
txdata=pd.read_pickle("D:/ica/tx0301.pkl")

data=pd.read_table('OWOSF_20170301.txt',names = ["日期", "商品代號","買賣別","委託量","未成交量","委託價","委託方式","單種","開平倉碼","委託時間","委託序號","減量口數","交易與委託報價檔連結代碼"])
u=data.loc[data['單種'] == 'U']
uu = u.reset_index(drop=True)
#只取txo部分
uu =uu.loc[uu['商品代號'].str[0:3]=='TXO']
uu = uu.reset_index(drop=True)

#buy = uu[uu.index%1==0]
buy = uu.loc[uu['買賣別'] == 'B']
buy = buy.reset_index(drop=True)
sell = uu.loc[uu['買賣別'] == 'S']
sell = sell.reset_index(drop=True)

spread = sell['委託價']-buy['委託價']

t_s=pd.DataFrame()
t_s['商品類別']=buy['商品代號'].str[8:10]
t_s['履約價']=buy['商品代號'].str[3:8].astype(int)#履約價 轉成int之後才會把開頭的0去掉!!
#t_s['委託量buy']=buy['委託量']##########b s不一定一樣多???
#t_s['委託量sell']=sell['委託量']##########b s不一定一樣多???
#t_s['未成交量']###
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
#建成要對上txo tx的key
#updated key
t_s['key']=t_s['商品類別']+'_'+t_s['履約價']+'_'+t_s['Time']

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

#merge完之後有些對不上
result_test = result_test.dropna(axis=0)#刪掉有na的row
result_test = result_test.reset_index(drop=True)

#整理一下把不要的column丟掉
#現在有兩個time 留一個就好
result_test = result_test.drop(columns=['履約日期','Contract','Date','Time_y'])
#統一RENAME
result_test = result_test.rename(columns={'Open':'Open_txo-1', 'High':'High_txo-1', 'Low':'Low_txo-1','Close':'Close_txo-1','Volume':'Volume_txo-1','Time_x':'Time'})

#抓tx資料
#只要留針對同一個時期的價格
#挑近月的 因為都取3月1日的所以都是201703到期的那一個
txtest = txdata.loc[txdata['Contract']=='201703']
#留需要的column就好
txtest = txtest.drop(columns=['Symbol','Contract','Date'])
#rename
txtest = txtest.rename(columns={'Open':'Open_tx-1', 'High':'High_tx-1', 'Low':'Low_tx-1','Close':'Close_tx-1','Volume':'Volume_tx-1'})
#merge
result_test = pd.merge(result_test, txtest, on=['Time'], how='left')
#merge完之後有些對不上 重新整理一下
result_test = result_test.dropna(axis=0)#刪掉有na的row
result_test = result_test.reset_index(drop=True)


result_test.to_pickle("D:/ica/0301data.pkl")#期交所台指期秒資料
