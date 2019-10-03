import xgboost as xgb

bst = xgb.Booster({'nthread': 4})  # init model
bst.load_model('../0001.model')  # load data


def main(ys, macd, sma, last_price):
    string = []
    for i in ys:
        string.append(i)
    for j in macd:
        string.append(j[0])
    for k in sma:
        string.append(k[0])
    string.append(last_price)
    #print (string)
    return bst.predict(xgb.DMatrix(string))
