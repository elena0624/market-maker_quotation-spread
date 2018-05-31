# market-maker_quotation-spread  
### steps:  
* define features & target
* data preprocessing
* building models
* try differnet models

### define features & target:
* all data in 2017/03/01
* target:  
    * txo/商品=/spread price  
    * both executed totally(or the narrowest)  
* features:  
    * ~~委託量~~  
    * txo price for 5 seconds
    * txo volume for 5 seconds
    * tx price for 5 seconds(?
    * tx volume for 5 seconds
    * strike price
    * seconds until executed
    * ~~委託價(本來應該用中價，先用委託買價代替)~~~ 改用委託中價 準確率降低
    * 減量口數????
    
### data preprocessing:
#### load data
* get txoosf u
* get txo seconds data
* get tx seconds data

#### data preprocessing
* compute whether both side has been totally executed or compute the narrowest spread for every merchandise in every second
* compute seconds before executed
* ~~merge u/txo data/tx data by merchandise type+strike time(A~L7 or M~X7)/strike price(ex. 9900)/time(ex. 08:59:40)~~
* merge u/txo data/tx data by merchandise type+strike time(A~L7 or M~X7)/strike price(ex. 9900)/time(ex. 08:59:40)=> time turns to be 5 seconds prior to current time
* so the key should have 5 

### building models:
* 3 layers of dense?


## 參考資料:
* 想要取最窄的spread: ~~https://medium.com/@kasiarachuta/dealing-with-duplicates-in-pandas-dataframe-789894a28911~~
* 想要取最窄的spread: group by

## 結果:
* 姑且先拿5秒/1秒/分買賣權/履約價來比較
